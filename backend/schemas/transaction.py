from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from decimal import Decimal
from datetime import datetime, date
import uuid
from models.transaction import TransactionType, ExpenseCategory


class TransactionBase(BaseModel):
    """Base transaction schema"""
    amount: Decimal = Field(..., gt=0)
    type: TransactionType
    category: Optional[ExpenseCategory] = None
    description: Optional[str] = Field(None, max_length=500)
    date: date

    @field_validator('category')
    @classmethod
    def validate_category(cls, v, info):
        if info.data.get('type') == TransactionType.EXPENSE and v is None:
            raise ValueError('Category is required for expense transactions')
        elif info.data.get('type') == TransactionType.INCOME and v is not None:
            raise ValueError('Category should not be set for income transactions')
        return v


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction"""
    pass


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction"""
    amount: Optional[Decimal] = Field(None, gt=0)
    type: Optional[TransactionType] = None
    category: Optional[ExpenseCategory] = None
    description: Optional[str] = Field(None, max_length=500)
    date: Optional[date] = None

    @field_validator('category')
    @classmethod
    def validate_category(cls, v, info):
        if info.data.get('type') == TransactionType.EXPENSE and v is None:
            raise ValueError('Category is required for expense transactions')
        elif info.data.get('type') == TransactionType.INCOME and v is not None:
            raise ValueError('Category should not be set for income transactions')
        return v


class TransactionResponse(TransactionBase):
    """Schema for transaction response"""
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TransactionList(BaseModel):
    """Schema for paginated transaction list"""
    transactions: List[TransactionResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

    class Config:
        from_attributes = True 