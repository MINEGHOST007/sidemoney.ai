from sqlalchemy import Column, String, Numeric, ARRAY, Text
from sqlalchemy.orm import relationship
from .base import BaseModel


class User(BaseModel):
    """User model for storing user profile and preferences"""
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    avatar_url = Column(Text, nullable=True)
    monthly_income = Column(Numeric(12, 2), nullable=True, default=0)
    preferred_spending_days = Column(ARRAY(String), nullable=True, default=list)
    daily_budget_multiplier = Column(Numeric(5, 2), nullable=True, default=1.0)
    current_amount = Column(Numeric(12, 2), nullable=False, default=0)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>" 