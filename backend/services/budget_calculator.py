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
        
        # Get basic info
        monthly_income = user.monthly_income or Decimal(0)
        current_amount = user.current_amount or Decimal(0)
        
        if not active_goals:
            # No goals - can spend entire monthly income
            days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
            day_of_month = current_date.day
            days_remaining_in_month = days_in_month - day_of_month + 1
            daily_budget = monthly_income / days_remaining_in_month if days_remaining_in_month > 0 else Decimal(0)
        else:
            # Find the earliest goal deadline to plan until that date
            earliest_deadline = min(goal.deadline for goal in active_goals if goal.deadline >= current_date)
            days_until_deadline = (earliest_deadline - current_date).days + 1  # Include today
            
            # Calculate total money available by deadline
            # Income payments: Get payment on 1st of each month
            months_until_deadline = 0
            temp_date = current_date
            while temp_date <= earliest_deadline:
                if temp_date.day == 1 or temp_date == current_date:  # Payment day or today
                    months_until_deadline += 1
                # Move to next month's 1st
                if temp_date.month == 12:
                    temp_date = temp_date.replace(year=temp_date.year + 1, month=1, day=1)
                else:
                    temp_date = temp_date.replace(month=temp_date.month + 1, day=1)
                    
            total_income_by_deadline = monthly_income * months_until_deadline
            total_available = current_amount + total_income_by_deadline
            
            # Calculate total needed for all active goals
            total_goals_amount = sum(goal.target_amount for goal in active_goals if goal.deadline >= current_date)
            
            # Calculate available for spending
            available_for_spending = total_available - total_goals_amount
            
            # Distribute across all days until deadline
            daily_budget = available_for_spending / days_until_deadline if days_until_deadline > 0 else Decimal(0)
        
        # Apply multiplier for preferred spending days
        multiplier = user.daily_budget_multiplier or Decimal(1.0)
        
        # Check if today is a preferred spending day
        today_name = current_date.strftime("%A")  # Gets day name like "Monday", "Tuesday", etc.
        preferred_days = user.preferred_spending_days or []
        is_preferred_day = today_name in preferred_days
        
        if is_preferred_day:
            # On preferred days: higher budget
            adjusted_daily_budget = daily_budget * multiplier
        else:
            # On non-preferred days: reduced budget to compensate
            # Formula: dailyBudget * (1 - (multiplier - 1) / 7)
            adjusted_daily_budget = daily_budget * (Decimal(1) - (multiplier - Decimal(1)) / Decimal(7))
        
        return {
            "daily_budget": float(daily_budget),
            "daily_budget_with_multiplier": float(adjusted_daily_budget),
            "monthly_income": float(monthly_income),
            "goal_contributions": float(total_goals_amount) if active_goals else 0,
            "available_for_spending": float(available_for_spending) if active_goals else float(monthly_income),
            "current_amount": float(current_amount),
            "days_remaining_in_month": calendar.monthrange(current_date.year, current_date.month)[1] - current_date.day + 1,
            "days_in_month": calendar.monthrange(current_date.year, current_date.month)[1],
            "is_preferred_day": is_preferred_day,
            "multiplier": float(multiplier),
            "days_until_deadline": days_until_deadline if active_goals else 0,
            "total_available_by_deadline": float(total_available) if active_goals else float(current_amount)
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
    
    @staticmethod
    def calculate_goal_progress(goal: Goal, current_amount: Decimal) -> Dict[str, Any]:
        """Calculate progress for a specific goal"""
        if not goal:
            return {
                "progress_percentage": 0,
                "amount_needed": 0,
                "is_achievable": False,
                "days_remaining": 0,
                "daily_savings_needed": 0
            }
        
        current_amount = current_amount or Decimal(0)
        target_amount = goal.target_amount or Decimal(0)
        
        # Calculate progress percentage
        progress_percentage = (current_amount / target_amount) * 100 if target_amount > 0 else 0
        progress_percentage = min(100, progress_percentage)  # Cap at 100%
        
        # Calculate amount still needed
        amount_needed = max(Decimal(0), target_amount - current_amount)
        
        # Calculate days remaining
        current_date = date.today()
        days_remaining = (goal.deadline - current_date).days if goal.deadline >= current_date else 0
        
        # Calculate daily savings needed
        daily_savings_needed = Decimal(0)
        if days_remaining > 0 and amount_needed > 0:
            daily_savings_needed = amount_needed / days_remaining
        
        # Check if goal is achievable (basic check)
        is_achievable = current_amount >= target_amount or days_remaining > 0
        
        return {
            "progress_percentage": float(progress_percentage),
            "amount_needed": float(amount_needed),
            "is_achievable": is_achievable,
            "days_remaining": days_remaining,
            "daily_savings_needed": float(daily_savings_needed),
            "status": "completed" if progress_percentage >= 100 else "in_progress" if progress_percentage > 0 else "not_started"
        } 