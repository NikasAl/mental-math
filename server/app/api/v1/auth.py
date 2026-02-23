from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models import User, UserProgress
from app.schemas.user import UserCreate, UserRead, Token, AccountLogin, UserProgressRead
from app.core.security import (
    create_access_token, decode_access_token, generate_account_key,
    get_password_hash, verify_password
)
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current user from JWT token."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


@router.post("/register", response_model=Token)
async def register(
    user_data: Optional[UserCreate] = None,
    db: AsyncSession = Depends(get_db)
):
    """Register new user with account_key (anonymous) or email/password."""
    if user_data and user_data.email and user_data.password:
        # Email/password registration
        result = await db.execute(select(User).where(User.email == user_data.email))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        account_key = generate_account_key()
        user = User(
            account_key=account_key,
            email=user_data.email,
            nickname=user_data.nickname,
            hashed_password=get_password_hash(user_data.password)
        )
    else:
        # Anonymous registration with account_key
        account_key = generate_account_key()
        user = User(account_key=account_key)
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Create progress record
    progress = UserProgress(user_id=user.id)
    db.add(progress)
    await db.commit()
    
    # Generate token
    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)


@router.post("/login", response_model=Token)
async def login(
    credentials: AccountLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login with account_key."""
    result = await db.execute(
        select(User).where(User.account_key == credentials.account_key)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid account key"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)


@router.post("/login-email", response_model=Token)
async def login_email(
    email: str,
    password: str,
    db: AsyncSession = Depends(get_db)
):
    """Login with email and password."""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if not user or not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)


@router.get("/me", response_model=UserRead)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """Get current user info."""
    return current_user


@router.get("/me/progress", response_model=UserProgressRead)
async def get_my_progress(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user progress."""
    result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == current_user.id)
    )
    progress = result.scalar_one_or_none()
    
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    return progress
