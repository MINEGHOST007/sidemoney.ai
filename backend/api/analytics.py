from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, extract
from typing import Dict, Any, Optional
from datetime import date, datetime, timedelta
from decimal import Decimal
import calendar

from database import get_db
from models.user import User
from models.transaction import Transaction, TransactionType, ExpenseCategory
from models.goal import Goal
from api.auth import get_current_user
from services.budget_calculator import BudgetCalculator
from services.ai_service import AIService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/daily-budget")
async def get_daily_budget(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Calculate current daily budget based on income and goals"""
    try:
        # Get active goals
        active_goals = db.query(Goal).filter(
            and_(Goal.user_id == current_user.id, Goal.deadline >= date.today())
        ).all()
        
        # Use BudgetCalculator service
        budget_info = BudgetCalculator.calculate_daily_budget(current_user, active_goals)
        
        # Add money needed per day calculation
        money_needed_info = BudgetCalculator.calculate_money_needed_per_day(current_user, active_goals)
        
        # Add goal information
        active_goals_count = len(active_goals)
        days_until_earliest_goal = None
        if active_goals:
            earliest_goal = min(active_goals, key=lambda g: g.deadline)
            days_until_earliest_goal = (earliest_goal.deadline - date.today()).days
        
        return {
            **budget_info,
            **money_needed_info,
            "active_goals_count": active_goals_count,
            "days_until_earliest_goal": days_until_earliest_goal
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate daily budget: {str(e)}"
        )


@router.get("/daily-report")
async def get_daily_report(
    report_date: Optional[date] = Query(None, description="Date for report (default: today)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-generated daily spending report"""
    if not report_date:
        report_date = date.today()
    
    try:
        # Get transactions for the day
        transactions = db.query(Transaction).filter(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.date == report_date
            )
        ).all()
        
        # Calculate totals
        total_income = sum(t.amount for t in transactions if t.type == TransactionType.INCOME)
        total_expenses = sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)
        net_change = total_income - total_expenses
        
        # Category breakdown for expenses
        category_breakdown = {}
        for transaction in transactions:
            if transaction.type == TransactionType.EXPENSE and transaction.category:
                category = transaction.category.value
                category_breakdown[category] = category_breakdown.get(category, 0) + float(transaction.amount)
        
        # Get daily budget for comparison using BudgetCalculator
        active_goals = db.query(Goal).filter(
            and_(Goal.user_id == current_user.id, Goal.deadline >= report_date)
        ).all()
        budget_info = BudgetCalculator.calculate_daily_budget(current_user, active_goals, report_date)
        daily_budget = budget_info["daily_budget_with_multiplier"]
        
        # Generate insights using AIService
        transaction_data = [
            {
                "amount": float(t.amount),
                "type": t.type.value,
                "category": t.category.value if t.category else None
            }
            for t in transactions
        ]
        insights = AIService.generate_spending_insights(transaction_data, daily_budget, 1)
        
        return {
            "date": report_date,
            "total_income": float(total_income),
            "total_expenses": float(total_expenses),
            "net_change": float(net_change),
            "daily_budget": daily_budget,
            "budget_remaining": daily_budget - float(total_expenses),
            "category_breakdown": category_breakdown,
            "transaction_count": len(transactions),
            "insights": insights
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate daily report: {str(e)}"
        )


@router.get("/monthly-report")
async def get_monthly_report(
    year: Optional[int] = Query(None, description="Year for report"),
    month: Optional[int] = Query(None, description="Month for report (1-12)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get monthly income vs expense summary"""
    if not year:
        year = date.today().year
    if not month:
        month = date.today().month
    
    try:
        # Get transactions for the month
        transactions = db.query(Transaction).filter(
            and_(
                Transaction.user_id == current_user.id,
                extract('year', Transaction.date) == year,
                extract('month', Transaction.date) == month
            )
        ).all()
        
        # Use BudgetCalculator service for analysis
        start_date = date(year, month, 1)
        end_date = date(year, month, calendar.monthrange(year, month)[1])
        analysis = BudgetCalculator.analyze_spending_pattern(transactions, start_date, end_date)
        
        # Daily breakdown
        daily_breakdown = {}
        for transaction in transactions:
            day = transaction.date.day
            if day not in daily_breakdown:
                daily_breakdown[day] = {"income": 0, "expenses": 0}
            
            if transaction.type == TransactionType.INCOME:
                daily_breakdown[day]["income"] += float(transaction.amount)
            else:
                daily_breakdown[day]["expenses"] += float(transaction.amount)
        
        return {
            "year": year,
            "month": month,
            **analysis,
            "daily_breakdown": daily_breakdown
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate monthly report: {str(e)}"
        )


@router.get("/category-breakdown")
async def get_category_breakdown(
    start_date: Optional[date] = Query(None, description="Start date"),
    end_date: Optional[date] = Query(None, description="End date"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get spending breakdown by category"""
    if not start_date:
        start_date = date.today() - timedelta(days=30)  # Last 30 days
    if not end_date:
        end_date = date.today()
    
    try:
        # Get expense transactions in date range
        expenses = db.query(Transaction).filter(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.type == TransactionType.EXPENSE,
                Transaction.date >= start_date,
                Transaction.date <= end_date
            )
        ).all()
        
        # Use BudgetCalculator service for analysis
        analysis = BudgetCalculator.analyze_spending_pattern(expenses, start_date, end_date)
        
        # Calculate percentages
        category_totals = analysis["category_breakdown"]
        total_expenses = analysis["total_expenses"]
        category_percentages = {}
        if total_expenses > 0:
            for category, amount in category_totals.items():
                category_percentages[category] = (amount / total_expenses) * 100
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_expenses": total_expenses,
            "category_totals": category_totals,
            "category_percentages": category_percentages,
            "transaction_count": len(expenses),
            "insights": analysis["insights"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                         detail=f"Failed to generate category breakdown: {str(e)}"
         )


@router.get("/goal-progress")
async def get_goal_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get progress tracking for all user goals"""
    try:
        # Get all user goals
        goals = db.query(Goal).filter(Goal.user_id == current_user.id).all()
        
        if not goals:
            return {
                "goals": [],
                "total_goals": 0,
                "overall_progress": 0
            }
        
        goal_progress = []
        total_progress = 0
        
        for goal in goals:
            progress = BudgetCalculator.calculate_goal_progress(goal, current_user.current_amount)
            goal_data = {
                "id": str(goal.id),
                "title": goal.title,
                "target_amount": float(goal.target_amount),
                "deadline": goal.deadline,
                "current_amount": float(current_user.current_amount),
                **progress
            }
            goal_progress.append(goal_data)
            total_progress += progress["progress_percentage"]
        
        # Calculate overall progress
        overall_progress = total_progress / len(goals) if goals else 0
        
        return {
            "goals": goal_progress,
            "total_goals": len(goals),
            "overall_progress": overall_progress
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate goal progress: {str(e)}"
        ) 