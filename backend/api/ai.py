from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date, timedelta
import logging

from database import get_db
from models.user import User
from models.transaction import Transaction
from models.goal import Goal
from api.auth import get_current_user
from services.ai_service import AIService
from schemas.ai import (
    AIAnalysisResponse, OCRResult, AIPromptRequest, AIPromptResponse
)

router = APIRouter(prefix="/ai", tags=["AI & Analytics"])
logger = logging.getLogger(__name__)


@router.post("/analyze", response_model=AIAnalysisResponse)
async def get_enhanced_financial_analysis(
    period_days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive AI-powered financial analysis with structured recommendations and insights"""
    
    try:
        # Get user's transactions for the period
        end_date = date.today()
        start_date = end_date - timedelta(days=period_days)
        
        transactions = db.query(Transaction).filter(
            Transaction.user_id == current_user.id,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).all()
        
        # Get user's goals
        goals = db.query(Goal).filter(Goal.user_id == current_user.id).all()
        
        # Prepare data for AI analysis
        user_spending = {}
        transaction_data = []
        
        for transaction in transactions:
            transaction_dict = {
                "id": str(transaction.id),
                "amount": float(transaction.amount),
                "type": transaction.type.value,
                "category": transaction.category.value if transaction.category else None,
                "description": transaction.description,
                "date": transaction.date.isoformat()
            }
            transaction_data.append(transaction_dict)
            
            if transaction.type.value == "expense" and transaction.category:
                category = transaction.category.value
                user_spending[category] = user_spending.get(category, 0) + float(transaction.amount)
        
        goals_data = []
        for goal in goals:
            # Calculate current progress based on user's current_amount
            # For simplicity, we'll assume each goal gets proportional share of user's current_amount
            progress_amount = 0.0
            if len(goals) > 0:
                progress_amount = float(current_user.current_amount) / len(goals)
            
            goal_dict = {
                "id": str(goal.id),
                "title": goal.title,
                "target_amount": float(goal.target_amount),
                "current_amount": min(progress_amount, float(goal.target_amount)),  # Use calculated progress
                "deadline": goal.deadline.isoformat(),
                "days_remaining": (goal.deadline - date.today()).days
            }
            goals_data.append(goal_dict)
        
        # Get daily budget based on monthly income and budget multiplier
        daily_budget = 50.0  # Default fallback
        if current_user.monthly_income and current_user.daily_budget_multiplier:
            # Calculate daily budget from monthly income
            monthly_budget = float(current_user.monthly_income) * float(current_user.daily_budget_multiplier)
            daily_budget = monthly_budget / 30  # Approximate daily budget
        elif current_user.monthly_income:
            # Use 30% of monthly income as default budget
            daily_budget = float(current_user.monthly_income) * 0.3 / 30
        
        # Generate enhanced analysis
        analysis = AIService.generate_enhanced_analysis(
            user_spending=user_spending,
            daily_budget=daily_budget,
            goals=goals_data,
            transactions=transaction_data,
            period_days=period_days
        )
        
        return analysis
        
    except Exception as e:
        logger.error(f"AI analysis failed for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate financial analysis"
        )


@router.post("/ocr", response_model=OCRResult)
async def process_receipt_ocr(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """Process receipt/document using OCR to extract transaction data"""
    
    # Validate file type - now accepting both images and PDFs
    if not file.content_type or not (
        file.content_type.startswith('image/') or 
        file.content_type == 'application/pdf'
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image (JPEG, PNG, etc.) or PDF document"
        )
    
    # Validate file size (10MB limit)
    max_size = 10 * 1024 * 1024  # 10MB
    
    try:
        # Read file content
        file_content = await file.read()
        
        if len(file_content) > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds 10MB limit"
            )
        
        # Process with OCR
        ocr_result = await AIService.process_receipt_ocr(
            image_data=file_content,
            filename=file.filename or "unknown"
        )
        
        logger.info(f"OCR processed {len(ocr_result.transactions)} transactions for user {current_user.id}")
        
        return ocr_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OCR processing failed for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}"
        )


@router.post("/query", response_model=AIPromptResponse)
async def custom_ai_query(
    request: AIPromptRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Ask custom questions to AI about your financial data"""
    
    try:
        # Gather user data based on request
        user_data = {}
        
        if request.include_budget:
            # Calculate daily budget from user's monthly income and multiplier
            daily_budget = 50.0  # Default fallback
            if current_user.monthly_income and current_user.daily_budget_multiplier:
                monthly_budget = float(current_user.monthly_income) * float(current_user.daily_budget_multiplier)
                daily_budget = monthly_budget / 30
            elif current_user.monthly_income:
                daily_budget = float(current_user.monthly_income) * 0.3 / 30
            
            user_data['daily_budget'] = daily_budget
        
        if request.include_transactions:
            end_date = date.today()
            start_date = end_date - timedelta(days=request.period_days)
            
            transactions = db.query(Transaction).filter(
                Transaction.user_id == current_user.id,
                Transaction.date >= start_date,
                Transaction.date <= end_date
            ).all()
            
            user_data['transactions'] = [
                {
                    "amount": float(t.amount),
                    "type": t.type.value,
                    "category": t.category.value if t.category else None,
                    "description": t.description,
                    "date": t.date.isoformat()
                }
                for t in transactions
            ]
        
        if request.include_goals:
            goals = db.query(Goal).filter(Goal.user_id == current_user.id).all()
            goals_list = []
            for g in goals:
                # Calculate progress for each goal
                progress_amount = 0.0
                if len(goals) > 0:
                    progress_amount = float(current_user.current_amount) / len(goals)
                
                goals_list.append({
                    "title": g.title,
                    "target_amount": float(g.target_amount),
                    "current_amount": min(progress_amount, float(g.target_amount)),
                    "deadline": g.deadline.isoformat(),
                    "days_remaining": (g.deadline - date.today()).days
                })
            user_data['goals'] = goals_list
        
        # Process with AI
        response = await AIService.custom_ai_query(request, user_data)
        
        return response
        
    except Exception as e:
        logger.error(f"Custom AI query failed for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process AI query"
        )
