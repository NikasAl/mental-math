from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class TaskBase(BaseModel):
    level: int
    sub_level: int = 1
    topic: str
    expression: str
    answer: str
    solution_steps: List[str] = []
    hint: Optional[str] = None


class TaskCreate(TaskBase):
    difficulty: int = 0
    is_ai_generated: bool = False


class TaskRead(TaskBase):
    id: int
    difficulty: int
    is_ai_generated: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TaskGenerateRequest(BaseModel):
    level: int
    sub_level: Optional[int] = None
    topic: Optional[str] = None


class TaskValidateRequest(BaseModel):
    task_id: int
    user_answer: str
    mental_steps: int = 0
    written_steps: int = 0
    time_seconds: int = 0
    hints_used: int = 0


class TaskValidateResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    xp_earned: int
    solution_steps: List[str]


class LevelInfo(BaseModel):
    level: int
    name: str
    description: str
    topics: List[str]


class LevelsResponse(BaseModel):
    levels: List[LevelInfo]
