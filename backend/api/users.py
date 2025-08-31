from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models.user import User
from models.transaction import Transaction
from models.goal import Goal
from schemas.user import UserUpdate, UserResponse, UserProfile
from api.auth import get_current_user

router = APIRouter(prefix="/user", tags=["User Profile"])


@router.get("/profile", response_model=UserProfile)
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user profile with computed statistics"""
    # Get transaction and goal counts
    total_transactions = db.query(func.count(Transaction.id)).filter(
        Transaction.user_id == current_user.id
    ).scalar() or 0
    
    total_goals = db.query(func.count(Goal.id)).filter(
        Goal.user_id == current_user.id
    ).scalar() or 0
    
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        avatar_url=current_user.avatar_url,
        monthly_income=current_user.monthly_income,
        preferred_spending_days=current_user.preferred_spending_days,
        daily_budget_multiplier=current_user.daily_budget_multiplier,
        current_amount=current_user.current_amount,
        total_goals=total_goals,
        total_transactions=total_transactions,
        created_at=current_user.created_at
    )


@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile information"""
    try:
        # Update only provided fields
        update_data = user_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(current_user, field, value)
        
        db.commit()
        db.refresh(current_user)
        
        return current_user
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile: {str(e)}"
        ) 