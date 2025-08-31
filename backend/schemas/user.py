from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
import uuid


class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)
    avatar_url: Optional[str] = None
    monthly_income: Optional[Decimal] = Field(default=0, ge=0)
    preferred_spending_days: Optional[List[str]] = Field(default_factory=list)
    daily_budget_multiplier: Optional[Decimal] = Field(default=1.0, ge=0.1, le=10.0)
    current_amount: Decimal = Field(default=0)

    @field_validator('preferred_spending_days')
    @classmethod
    def validate_spending_days(cls, v):
        valid_days = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}
        if v:
            for day in v:
                if day not in valid_days:
                    raise ValueError(f'Invalid day: {day}. Must be one of {valid_days}')
        return v


class UserCreate(UserBase):
    """Schema for creating a new user"""
    pass


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    monthly_income: Optional[Decimal] = Field(None, ge=0)
    preferred_spending_days: Optional[List[str]] = None
    daily_budget_multiplier: Optional[Decimal] = Field(None, ge=0.1, le=10.0)
    current_amount: Optional[Decimal] = None

    @field_validator('preferred_spending_days')
    @classmethod
    def validate_spending_days(cls, v):
        if v is not None:
            valid_days = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}
            for day in v:
                if day not in valid_days:
                    raise ValueError(f'Invalid day: {day}. Must be one of {valid_days}')
        return v


class UserResponse(UserBase):
    """Schema for user response"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """Schema for user profile with computed fields"""
    id: uuid.UUID
    email: EmailStr
    name: str
    avatar_url: Optional[str]
    monthly_income: Optional[Decimal]
    preferred_spending_days: Optional[List[str]]
    daily_budget_multiplier: Optional[Decimal]
    current_amount: Decimal
    total_goals: int
    total_transactions: int
    created_at: datetime

    class Config:
        from_attributes = True 