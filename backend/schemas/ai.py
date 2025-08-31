from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from decimal import Decimal
from datetime import date as Date
from enum import Enum
from models.transaction import TransactionType, ExpenseCategory


class RecommendationType(str, Enum):
    """Types of financial recommendations"""
    BUDGET_OPTIMIZATION = "budget_optimization"
    CATEGORY_REDUCTION = "category_reduction"
    SAVINGS_INCREASE = "savings_increase"
    GOAL_ACCELERATION = "goal_acceleration"
    SPENDING_PATTERN = "spending_pattern"


class RecommendationPriority(str, Enum):
    """Priority levels for recommendations"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class FinancialRecommendation(BaseModel):
    """Structured financial recommendation"""
    title: str = Field(..., description="Brief title of the recommendation")
    description: str = Field(..., description="Detailed recommendation text")
    type: RecommendationType = Field(..., description="Type of recommendation")
    priority: RecommendationPriority = Field(..., description="Priority level")
    potential_savings: Optional[Decimal] = Field(None, description="Estimated monthly savings in dollars")
    action_items: List[str] = Field(default_factory=list, description="Specific action steps")
    category_focus: Optional[ExpenseCategory] = Field(None, description="Related expense category if applicable")


class SpendingInsight(BaseModel):
    """Structured spending insight"""
    insight_type: str = Field(..., description="Type of insight (trend, pattern, comparison)")
    title: str = Field(..., description="Brief insight title")
    description: str = Field(..., description="Detailed insight description")
    metric_value: Optional[float] = Field(None, description="Numerical value if applicable")
    metric_unit: Optional[str] = Field(None, description="Unit of measurement")
    trend_direction: Optional[str] = Field(None, description="up, down, or stable")
    severity: Optional[str] = Field(None, description="low, medium, high")


class AIAnalysisResponse(BaseModel):
    """Complete AI analysis response"""
    recommendations: List[FinancialRecommendation] = Field(default_factory=list)
    insights: List[SpendingInsight] = Field(default_factory=list)
    summary: str = Field(..., description="Overall financial health summary")
    confidence_score: float = Field(..., ge=0, le=1, description="AI confidence in analysis")


class OCRTransactionItem(BaseModel):
    """Single transaction extracted from OCR"""
    description: str = Field(..., description="Transaction description")
    amount: Decimal = Field(..., gt=0, description="Transaction amount")
    date: Date = Field(..., description="Transaction date")
    category: Optional[ExpenseCategory] = Field(None, description="Auto-categorized expense category")
    merchant: Optional[str] = Field(None, description="Merchant name if identifiable")
    confidence: float = Field(..., ge=0, le=1, description="OCR extraction confidence")


class OCRResult(BaseModel):
    """OCR processing result"""
    transactions: List[OCRTransactionItem] = Field(default_factory=list)
    total_amount: Decimal = Field(default=0, description="Total amount extracted")
    document_type: str = Field(..., description="Type of document processed (receipt, bank_statement, etc.)")
    processing_confidence: float = Field(..., ge=0, le=1, description="Overall processing confidence")
    raw_text: Optional[str] = Field(None, description="Raw extracted text for review")
    warnings: List[str] = Field(default_factory=list, description="Processing warnings or issues")


class BulkTransactionCreate(BaseModel):
    """Schema for bulk transaction creation"""
    transactions: List[OCRTransactionItem] = Field(..., min_items=1, max_items=100)
    source: str = Field(default="ocr", description="Source of transactions")
    verify_before_save: bool = Field(default=True, description="Whether to return for user verification first")


class BulkTransactionResponse(BaseModel):
    """Response for bulk transaction creation"""
    created_count: int = Field(..., description="Number of transactions created")
    failed_count: int = Field(default=0, description="Number of transactions that failed")
    transaction_ids: List[str] = Field(default_factory=list, description="IDs of created transactions")
    errors: List[str] = Field(default_factory=list, description="Error messages for failed transactions")


class AIPromptRequest(BaseModel):
    """Request for custom AI analysis"""
    user_query: str = Field(..., description="User's question or request")
    include_transactions: bool = Field(default=True, description="Include recent transaction data")
    include_goals: bool = Field(default=True, description="Include user goals")
    include_budget: bool = Field(default=True, description="Include budget information")
    period_days: int = Field(default=30, ge=1, le=365, description="Analysis period in days")


class AIPromptResponse(BaseModel):
    """Response for custom AI analysis"""
    response: str = Field(..., description="AI-generated response")
    data_sources: List[str] = Field(default_factory=list, description="Data sources used in analysis")
    suggestions: List[str] = Field(default_factory=list, description="Additional suggestions")
    confidence: float = Field(..., ge=0, le=1, description="Response confidence") 