from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from decimal import Decimal
from datetime import datetime, date
import uuid


class GoalBase(BaseModel):
    """Base goal schema"""
    title: str = Field(..., min_length=1, max_length=255)
    target_amount: Decimal = Field(..., gt=0)
    deadline: date

    @field_validator('target_amount', mode='before')
    @classmethod
    def convert_target_amount_to_decimal(cls, v):
        if isinstance(v, (int, float)):
            return Decimal(str(v))
        return v

    @field_validator('deadline')
    @classmethod
    def validate_deadline(cls, v):
        if v <= date.today():
            raise ValueError('Deadline must be in the future')
        return v


class GoalCreate(GoalBase):
    """Schema for creating a new goal"""
    pass


class GoalUpdate(BaseModel):
    """Schema for updating a goal"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    target_amount: Optional[Decimal] = Field(None, gt=0)
    deadline: Optional[date] = None

    @field_validator('target_amount', mode='before')
    @classmethod
    def convert_target_amount_to_decimal(cls, v):
        if v is not None and isinstance(v, (int, float)):
            return Decimal(str(v))
        return v

    @field_validator('deadline')
    @classmethod
    def validate_deadline(cls, v):
        if v is not None and v <= date.today():
            raise ValueError('Deadline must be in the future')
        return v


class GoalResponse(GoalBase):
    """Schema for goal response"""
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GoalList(BaseModel):
    """Schema for goal list response"""
    goals: List[GoalResponse]
    total: int

    class Config:
        from_attributes = True 