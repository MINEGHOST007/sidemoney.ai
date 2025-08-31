from sqlalchemy import Column, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import BaseModel


class Goal(BaseModel):
    """Goal model for financial goal tracking"""
    __tablename__ = "goals"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    target_amount = Column(Numeric(12, 2), nullable=False)
    deadline = Column(Date, nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="goals")
    
    def __repr__(self):
        return f"<Goal(id={self.id}, title={self.title}, target_amount={self.target_amount}, user_id={self.user_id})>" 