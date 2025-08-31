from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import Optional, List
from datetime import date, datetime
import uuid
import math
import logging

from database import get_db
from models.user import User
from models.transaction import Transaction, TransactionType, ExpenseCategory
from schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse, TransactionList
from schemas.ai import BulkTransactionCreate, BulkTransactionResponse, OCRTransactionItem
from api.auth import get_current_user
from services.ai_service import AIService

router = APIRouter(prefix="/transactions", tags=["Transactions"])
logger = logging.getLogger(__name__)


@router.get("", response_model=TransactionList)
async def get_transactions(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    transaction_type: Optional[TransactionType] = Query(None, description="Filter by transaction type"),
    category: Optional[ExpenseCategory] = Query(None, description="Filter by category"),
    start_date: Optional[date] = Query(None, description="Start date filter"),
    end_date: Optional[date] = Query(None, description="End date filter"),
    search: Optional[str] = Query(None, description="Search in description"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get paginated list of user transactions with filters"""
    # Build query
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)
    
    # Apply filters
    if transaction_type:
        query = query.filter(Transaction.type == transaction_type)
    
    if category:
        query = query.filter(Transaction.category == category)
    
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    if search:
        query = query.filter(Transaction.description.ilike(f"%{search}%"))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * per_page
    transactions = query.order_by(desc(Transaction.date), desc(Transaction.created_at)).offset(offset).limit(per_page).all()
    
    # Calculate total pages
    total_pages = math.ceil(total / per_page)
    
    return TransactionList(
        transactions=transactions,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )


@router.post("", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new transaction"""
    try:
        # Auto-categorize if it's an expense and no category provided
        transaction_data = transaction.dict()
        if (transaction.type == TransactionType.EXPENSE and 
            not transaction_data.get('category') and 
            transaction_data.get('description')):
            suggested_category = AIService.categorize_transaction(transaction_data['description'])
            transaction_data['category'] = suggested_category
        
        # Create new transaction
        db_transaction = Transaction(
            user_id=current_user.id,
            **transaction_data
        )
        
        # Update user's current amount
        if transaction.type == TransactionType.INCOME:
            current_user.current_amount += transaction.amount
        else:  # EXPENSE
            current_user.current_amount -= transaction.amount
        
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        
        return db_transaction
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create transaction: {str(e)}"
        )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific transaction by ID"""
    transaction = db.query(Transaction).filter(
        and_(Transaction.id == transaction_id, Transaction.user_id == current_user.id)
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: uuid.UUID,
    transaction_update: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a specific transaction"""
    # Get existing transaction
    db_transaction = db.query(Transaction).filter(
        and_(Transaction.id == transaction_id, Transaction.user_id == current_user.id)
    ).first()
    
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    try:
        # Store old values for amount adjustment
        old_amount = db_transaction.amount
        old_type = db_transaction.type
        
        # Update transaction fields
        update_data = transaction_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_transaction, field, value)
        
        # Adjust user's current amount
        # Revert old transaction effect
        if old_type == TransactionType.INCOME:
            current_user.current_amount -= old_amount
        else:
            current_user.current_amount += old_amount
        
        # Apply new transaction effect
        if db_transaction.type == TransactionType.INCOME:
            current_user.current_amount += db_transaction.amount
        else:
            current_user.current_amount -= db_transaction.amount
        
        db.commit()
        db.refresh(db_transaction)
        
        return db_transaction
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update transaction: {str(e)}"
        )


@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific transaction"""
    transaction = db.query(Transaction).filter(
        and_(Transaction.id == transaction_id, Transaction.user_id == current_user.id)
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    try:
        # Revert transaction effect on user's current amount
        if transaction.type == TransactionType.INCOME:
            current_user.current_amount -= transaction.amount
        else:
            current_user.current_amount += transaction.amount
        
        db.delete(transaction)
        db.commit()
        
        return {"message": "Transaction deleted successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete transaction: {str(e)}"
        )


@router.post("/bulk", response_model=BulkTransactionResponse)
async def create_bulk_transactions(
    bulk_request: BulkTransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create multiple transactions from OCR results or bulk import"""
    
    created_transactions = []
    failed_transactions = []
    errors = []
    
    try:
        for ocr_transaction in bulk_request.transactions:
            try:
                # Create transaction model
                transaction = Transaction(
                    user_id=current_user.id,
                    amount=ocr_transaction.amount,
                    type=TransactionType.EXPENSE,  # OCR typically processes expenses
                    category=ocr_transaction.category or ExpenseCategory.MISCELLANEOUS,
                    description=ocr_transaction.description,
                    date=ocr_transaction.date
                )
                
                db.add(transaction)
                db.flush()  # Get ID without committing
                created_transactions.append(str(transaction.id))
                
            except Exception as e:
                failed_transactions.append(ocr_transaction.description)
                errors.append(f"Failed to create transaction '{ocr_transaction.description}': {str(e)}")
                logger.warning(f"Failed to create transaction for user {current_user.id}: {e}")
                
        # Commit all successful transactions
        if created_transactions:
            db.commit()
            logger.info(f"Created {len(created_transactions)} transactions for user {current_user.id}")
        else:
            db.rollback()
        
        return BulkTransactionResponse(
            created_count=len(created_transactions),
            failed_count=len(failed_transactions),
            transaction_ids=created_transactions,
            errors=errors
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"Bulk transaction creation failed for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create bulk transactions"
        )


@router.post("/categorize")
async def categorize_transaction_description(
    description: str = Query(..., description="Transaction description"),
    amount: Optional[float] = Query(None, description="Transaction amount for better categorization"),
    current_user: User = Depends(get_current_user)
):
    """Get AI-suggested category for a transaction description"""
    try:
        suggested_category = AIService.categorize_transaction(description, amount)
        return {
            "description": description,
            "suggested_category": suggested_category.value,
            "category_display_name": suggested_category.value.replace('_', ' ').title(),
            "confidence": "high" if suggested_category != ExpenseCategory.MISCELLANEOUS else "low"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to categorize transaction: {str(e)}"
        )


 