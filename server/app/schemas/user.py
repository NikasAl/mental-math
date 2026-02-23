from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    nickname: Optional[str] = None
    email: Optional[str] = None


class UserCreate(UserBase):
    account_key: Optional[str] = None
    password: Optional[str] = None


class UserRead(UserBase):
    id: int
    account_key: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserProgressRead(BaseModel):
    current_level: int
    current_sub_level: int
    level_progress: int
    total_xp: int
    total_tasks: int
    correct_tasks: int
    streak_days: int
    last_activity: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AccountLogin(BaseModel):
    account_key: str
