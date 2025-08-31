from pydantic import BaseModel
from typing import Optional
import uuid


class Token(BaseModel):
    """JWT token response schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: uuid.UUID


class TokenData(BaseModel):
    """Token data for JWT payload"""
    user_id: Optional[uuid.UUID] = None
    email: Optional[str] = None


class GoogleAuthRequest(BaseModel):
    """Google OAuth authentication request"""
    id_token: str 