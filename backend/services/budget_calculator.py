from decimal import Decimal
from datetime import date, timedelta
from typing import List, Dict, Any
import calendar

from models.user import User
from models.goal import Goal
from models.transaction import Transaction, TransactionType


class BudgetCalculator:
    """Service for budget calculations and financial logic"""
    
    @staticmethod
    def calculate_daily_budget(
        user: User, 
        active_goals: List[Goal], 
        current_date: date = None
    ) -> Dict[str, Any]:
        """Calculate daily budget based on current amount, income and goals"""
        if not current_date:
            current_date = date.today()
        
        # Get days remaining in current month
        days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
        day_of_month = current_date.day
        days_remaining_in_month = days_in_month - day_of_month + 1
        
        # Calculate total amount still needed for goals
        total_goal_shortfall = Decimal(0)
        for goal in active_goals:
            if goal.deadline >= current_date:
                # Consider current amount when calculating goal shortfall
                goal_shortfall = max(Decimal(0), goal.target_amount - user.current_amount)
                days_until_deadline = (goal.deadline - current_date).days
                if days_until_deadline > 0:
                    # Distribute shortfall over remaining time
                    months_remaining = max(1, days_until_deadline // 30 + 1)
                    monthly_contribution = goal_shortfall / months_remaining
                    total_goal_shortfall += monthly_contribution
        
        # Calculate available spending money considering current amount
        monthly_income = user.monthly_income or Decimal(0)
        current_amount = user.current_amount or Decimal(0)
        
        # Available for spending = income - goal contributions
        available_for_spending = monthly_income - total_goal_shortfall
        
        # Calculate base daily budget for remaining days in month
        daily_budget = available_for_spending / days_remaining_in_month if days_remaining_in_month > 0 else Decimal(0)
        
        # Apply multiplier for preferred spending days
        multiplier = user.daily_budget_multiplier or Decimal(1.0)
        adjusted_daily_budget = daily_budget * multiplier
        
        return {
            "daily_budget": float(daily_budget),
            "daily_budget_with_multiplier": float(adjusted_daily_budget),
            "monthly_income": float(monthly_income),
            "goal_contributions": float(total_goal_shortfall),
            "available_for_spending": float(available_for_spending),
            "current_amount": float(current_amount),
            "days_remaining_in_month": days_remaining_in_month,
            "days_in_month": days_in_month
        }
    
    @staticmethod
    def calculate_money_needed_per_day(
        user: User, 
        goals: List[Goal], 
        current_date: date = None
    ) -> Dict[str, Any]:
        """Calculate how much money user needs to earn per day to reach goals"""
        if not current_date:
            current_date = date.today()
        
        # Calculate total amount needed for all goals
        total_needed = Decimal(0)
        earliest_deadline = None
        
        for goal in goals:
            if goal.deadline >= current_date:
                total_needed += goal.target_amount
                if earliest_deadline is None or goal.deadline < earliest_deadline:
                    earliest_deadline = goal.deadline
        
        if not earliest_deadline:
            return {
                "money_needed_per_day": 0,
                "total_needed": 0,
                "days_remaining": 0,
                "current_amount": float(user.current_amount),
                "shortfall": 0
            }
        
        # Calculate days remaining until earliest deadline
        days_remaining = (earliest_deadline - current_date).days
        
        # Calculate shortfall considering current amount
        current_amount = user.current_amount or Decimal(0)
        shortfall = max(Decimal(0), total_needed - current_amount)
        
        # Calculate money needed per day (only if there's a shortfall)
        money_needed_per_day = shortfall / days_remaining if days_remaining > 0 and shortfall > 0 else Decimal(0)
        
        return {
            "money_needed_per_day": float(money_needed_per_day),
            "total_needed": float(total_needed),
            "days_remaining": days_remaining,
            "current_amount": float(current_amount),
            "shortfall": float(shortfall),
            "earliest_deadline": earliest_deadline
        }
    
    @staticmethod
    def analyze_spending_pattern(
        transactions: List[Transaction], 
        start_date: date, 
        end_date: date
    ) -> Dict[str, Any]:
        """Analyze spending patterns and trends"""
        if not transactions:
            return {
                "total_income": 0,
                "total_expenses": 0,
                "net_change": 0,
                "average_daily_expense": 0,
                "category_breakdown": {},
                "insights": []
            }
        
        # Calculate totals
        total_income = sum(t.amount for t in transactions if t.type == TransactionType.INCOME)
        total_expenses = sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)
        net_change = total_income - total_expenses
        
        # Calculate average daily expense
        days_in_period = (end_date - start_date).days + 1
        average_daily_expense = total_expenses / days_in_period if days_in_period > 0 else Decimal(0)
        
        # Category breakdown
        category_breakdown = {}
        for transaction in transactions:
            if transaction.type == TransactionType.EXPENSE and transaction.category:
                category = transaction.category.value
                category_breakdown[category] = category_breakdown.get(category, 0) + float(transaction.amount)
        
        # Generate insights
        insights = []
        if category_breakdown:
            top_category = max(category_breakdown.items(), key=lambda x: x[1])
            insights.append(f"Your highest spending category is {top_category[0].replace('_', ' ').title()}")
            
            if len(category_breakdown) > 1:
                sorted_categories = sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True)
                insights.append(f"Top 3 categories: {', '.join([cat[0].replace('_', ' ').title() for cat in sorted_categories[:3]])}")
        
        if net_change > 0:
            insights.append(f"You saved ${net_change:.2f} during this period")
        elif net_change < 0:
            insights.append(f"You spent ${abs(net_change):.2f} more than you earned")
        
        return {
            "total_income": float(total_income),
            "total_expenses": float(total_expenses),
            "net_change": float(net_change),
            "average_daily_expense": float(average_daily_expense),
            "category_breakdown": category_breakdown,
            "insights": insights
        } 