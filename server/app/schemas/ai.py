from typing import List, Optional
from pydantic import BaseModel


class AIHintRequest(BaseModel):
    task_id: int
    current_step: Optional[int] = None
    context: Optional[str] = None


class AIHintResponse(BaseModel):
    hint: str
    is_final: bool


class AIExplanationRequest(BaseModel):
    task_id: int
    user_answer: Optional[str] = None
    request_detailed: bool = False


class AIExplanationResponse(BaseModel):
    explanation: str
    mental_method: str
    common_mistakes: List[str]


class AITaskGenerateRequest(BaseModel):
    level: int
    sub_level: int = 1
    topic: Optional[str] = None
    count: int = 1


class AITaskGenerateResponse(BaseModel):
    expression: str
    answer: str
    solution_steps: List[str]
    hint: Optional[str] = None
