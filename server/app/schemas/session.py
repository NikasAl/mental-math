from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class TaskSessionBase(BaseModel):
    task_id: int
    user_answer: Optional[str] = None
    is_correct: bool = False
    mental_steps: int = 0
    written_steps: int = 0
    time_seconds: int = 0
    xp_earned: int = 0
    hints_used: int = 0


class TaskSessionRead(TaskSessionBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SessionStats(BaseModel):
    total_sessions: int
    correct_sessions: int
    total_xp: int
    avg_time_seconds: float
    accuracy: float


class ProgressResponse(BaseModel):
    current_level: int
    current_sub_level: int
    level_progress: int
    total_xp: int
    total_tasks: int
    correct_tasks: int
    streak_days: int
    accuracy: float
    next_level_xp: int
