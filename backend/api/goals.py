from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import List
import uuid

from database import get_db
from models.user import User
from models.goal import Goal
from schemas.goal import GoalCreate, GoalUpdate, GoalResponse, GoalList
from api.auth import get_current_user

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.get("", response_model=GoalList)
async def get_goals(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all user goals"""
    goals = db.query(Goal).filter(Goal.user_id == current_user.id).order_by(Goal.deadline).all()
    total = len(goals)
    
    return GoalList(goals=goals, total=total)


@router.post("", response_model=GoalResponse)
async def create_goal(
    goal: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new financial goal"""
    try:
        db_goal = Goal(
            user_id=current_user.id,
            **goal.dict()
        )
        
        db.add(db_goal)
        db.commit()
        db.refresh(db_goal)
        
        return db_goal
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create goal: {str(e)}"
        )


@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(
    goal_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific goal by ID"""
    goal = db.query(Goal).filter(
        and_(Goal.id == goal_id, Goal.user_id == current_user.id)
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    return goal


@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: uuid.UUID,
    goal_update: GoalUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a specific goal"""
    db_goal = db.query(Goal).filter(
        and_(Goal.id == goal_id, Goal.user_id == current_user.id)
    ).first()
    
    if not db_goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    try:
        # Update goal fields
        update_data = goal_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_goal, field, value)
        
        db.commit()
        db.refresh(db_goal)
        
        return db_goal
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update goal: {str(e)}"
        )


@router.delete("/{goal_id}")
async def delete_goal(
    goal_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific goal"""
    goal = db.query(Goal).filter(
        and_(Goal.id == goal_id, Goal.user_id == current_user.id)
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    try:
        db.delete(goal)
        db.commit()
        
        return {"message": "Goal deleted successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete goal: {str(e)}"
        ) 