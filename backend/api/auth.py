from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
import jwt
from datetime import datetime, timedelta
import os
from google.oauth2 import id_token
from google.auth.transport import requests
import uuid

from database import get_db
from models.user import User
from schemas.auth import Token, TokenData, GoogleAuthRequest
from schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """Verify JWT token and return token data"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token_data = TokenData(user_id=uuid.UUID(user_id), email=email)
        return token_data
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token_data: TokenData = Depends(verify_token), db: Session = Depends(get_db)) -> User:
    """Get current authenticated user"""
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user


@router.post("/google", response_model=Token)
async def google_auth(auth_request: GoogleAuthRequest, db: Session = Depends(get_db)):
    """Authenticate user with Google OAuth"""
    try:
        # Verify Google ID token
        idinfo = id_token.verify_oauth2_token(
            auth_request.id_token, 
            requests.Request(), 
            GOOGLE_CLIENT_ID
        )
        
        # Extract user information
        email = idinfo.get('email')
        name = idinfo.get('name')
        avatar_url = idinfo.get('picture')
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not found in Google token"
            )
        
        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # Create new user
            user_data = UserCreate(
                email=email,
                name=name or email.split('@')[0],
                avatar_url=avatar_url
            )
            user = User(**user_data.dict())
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
            user_id=user.id
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid Google token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout user (client should delete token)"""
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user 