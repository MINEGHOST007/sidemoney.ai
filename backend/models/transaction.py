from sqlalchemy import Column, String, Numeric, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
from .base import BaseModel


class TransactionType(str, Enum):
    """Transaction type enumeration"""
    INCOME = "income"
    EXPENSE = "expense"


class ExpenseCategory(str, Enum):
    """Expense category enumeration"""
    FOOD_DINING = "FOOD_DINING"
    GROCERIES = "GROCERIES"
    TRANSPORTATION = "TRANSPORTATION"
    SHOPPING = "SHOPPING"
    ENTERTAINMENT = "ENTERTAINMENT"
    BILLS_UTILITIES = "BILLS_UTILITIES"
    HEALTHCARE = "HEALTHCARE"
    EDUCATION = "EDUCATION"
    TRAVEL = "TRAVEL"
    FITNESS = "FITNESS"
    PERSONAL_CARE = "PERSONAL_CARE"
    GIFTS_DONATIONS = "GIFTS_DONATIONS"
    BUSINESS = "BUSINESS"
    MISCELLANEOUS = "MISCELLANEOUS"


class Transaction(BaseModel):
    """Transaction model for income and expense tracking"""
    __tablename__ = "transactions"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    type = Column(SQLEnum(TransactionType), nullable=False)
    category = Column(SQLEnum(ExpenseCategory), nullable=True)  # Only for expenses
    description = Column(String(500), nullable=True)
    date = Column(Date, nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.type}, amount={self.amount}, user_id={self.user_id})>" 