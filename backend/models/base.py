from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String

Base = declarative_base()


class BaseModel(Base):
    """Abstract base model with common fields"""
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>" 