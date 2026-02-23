import random
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models import Task, TaskSession, User, UserProgress
from app.schemas.task import (
    TaskRead, TaskGenerateRequest, TaskValidateRequest,
    TaskValidateResponse, LevelsResponse, LevelInfo
)
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


# Level definitions
LEVELS = [
    LevelInfo(
        level=1, 
        name="Элементарная арифметика",
        description="Сложение/вычитание двузначных чисел, умножение/деление на однозначное",
        topics=["сложение", "вычитание", "умножение", "деление"]
    ),
    LevelInfo(
        level=2,
        name="Устный счёт",
        description="Умножение двузначных, деление с остатком, простые дроби",
        topics=["умножение_двузначных", "деление_остаток", "дроби"]
    ),
    LevelInfo(
        level=3,
        name="Алгебраические преобразования",
        description="Раскрытие скобок, формулы сокращённого умножения",
        topics=["скобки", "фсу", "упрощение"]
    ),
    LevelInfo(
        level=4,
        name="Уравнения и неравенства",
        description="Линейные и квадратные уравнения",
        topics=["линейные", "квадратные", "системы"]
    ),
    LevelInfo(
        level=5,
        name="Функции и графики",
        description="Исследование функций, производные",
        topics=["функции", "графики", "производные"]
    ),
    LevelInfo(
        level=6,
        name="Тригонометрия",
        description="Тригонометрические тождества и преобразования",
        topics=["тождества", "преобразования"]
    ),
    LevelInfo(
        level=7,
        name="Логарифмы и степени",
        description="Свойства логарифмов, показательные уравнения",
        topics=["логарифмы", "степени", "показательные"]
    ),
    LevelInfo(
        level=8,
        name="Интегралы и производные",
        description="Табличные интегралы, правила дифференцирования",
        topics=["интегралы", "дифференцирование"]
    ),
    LevelInfo(
        level=9,
        name="Сложные выражения",
        description="Многоэтажные дроби, радикалы, комплексные преобразования",
        topics=["радикалы", "дроби_сложные", "преобразования"]
    ),
    LevelInfo(
        level=10,
        name="Олимпиадные задачи",
        description="Задачи уровня Сканави, Демидовича",
        topics=["олимпиады", "нестандартные", "комбинированные"]
    ),
]


@router.get("/levels", response_model=LevelsResponse)
async def get_levels():
    """Get list of all difficulty levels."""
    return LevelsResponse(levels=LEVELS)


@router.get("/topics")
async def get_topics(level: Optional[int] = None):
    """Get list of topics, optionally filtered by level."""
    if level is not None:
        if 1 <= level <= 10:
            return {"topics": LEVELS[level - 1].topics}
        raise HTTPException(status_code=400, detail="Invalid level")
    return {"topics": [topic for lv in LEVELS for topic in lv.topics]}


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific task by ID."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/", response_model=List[TaskRead])
async def list_tasks(
    level: Optional[int] = None,
    topic: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """List tasks with optional filters."""
    query = select(Task)
    
    if level is not None:
        query = query.where(Task.level == level)
    if topic:
        query = query.where(Task.topic == topic)
    
    query = query.order_by(Task.id.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/generate", response_model=TaskRead)
async def generate_task(
    request: TaskGenerateRequest,
    db: AsyncSession = Depends(get_db)
):
    """Generate a new task for given level."""
    sub_level = request.sub_level or random.randint(1, 10)
    
    # Template-based generation for levels 1-3
    if request.level <= 3:
        task = await _generate_template_task(request.level, sub_level, request.topic, db)
    else:
        # For higher levels, use AI generation (placeholder for now)
        task = await _generate_ai_task(request.level, sub_level, request.topic, db)
    
    return task


async def _generate_template_task(
    level: int, 
    sub_level: int, 
    topic: Optional[str],
    db: AsyncSession
) -> Task:
    """Generate task using templates for simple levels."""
    
    if level == 1:
        # Simple arithmetic
        if topic == "вычитание" or (topic is None and random.random() < 0.25):
            a = random.randint(10 + sub_level * 5, 50 + sub_level * 10)
            b = random.randint(5, a - 5)
            answer = a - b
            expression = f"{a} - {b}"
            steps = [f"Вычитаем {b} из {a}", f"Результат: {answer}"]
        elif topic == "умножение" or (topic is None and random.random() < 0.33):
            a = random.randint(2, 9)
            b = random.randint(10 + sub_level * 2, 20 + sub_level * 5)
            answer = a * b
            expression = f"{a} \\times {b}"
            steps = [f"Умножаем {a} на {b}", f"Результат: {answer}"]
        elif topic == "деление" or (topic is None and random.random() < 0.5):
            b = random.randint(2, 9)
            answer = random.randint(2, 10 + sub_level)
            a = b * answer
            expression = f"{a} \\div {b}"
            steps = [f"Делим {a} на {b}", f"Результат: {answer}"]
        else:
            # Addition
            a = random.randint(10 + sub_level * 5, 50 + sub_level * 10)
            b = random.randint(10 + sub_level * 5, 50 + sub_level * 10)
            answer = a + b
            expression = f"{a} + {b}"
            steps = [f"Складываем {a} и {b}", f"Результат: {answer}"]
        
        topic_used = topic or random.choice(["сложение", "вычитание", "умножение", "деление"])
        
    elif level == 2:
        # Two-digit multiplication
        a = random.randint(11, 20 + sub_level * 3)
        b = random.randint(11, 20 + sub_level * 3)
        answer = a * b
        
        # Show a mental math trick in steps
        a_rounded = ((a + 4) // 5) * 5  # Round to nearest 5
        diff = a - a_rounded
        
        expression = f"{a} \\times {b}"
        steps = [
            f"Разложим {a} = {a_rounded} + {(-diff) if diff < 0 else diff}",
            f"{a_rounded} × {b} = {a_rounded * b}",
            f"{'Вычитаем' if diff < 0 else 'Добавляем'} {abs(diff * b)}",
            f"Результат: {answer}"
        ]
        topic_used = topic or "умножение_двузначных"
        
    else:
        # Level 3 - Algebra
        a = random.randint(2, 5 + sub_level)
        b = random.randint(2, 5 + sub_level)
        answer = f"2 \\cdot {a} \\cdot {b} = {2*a*b}"
        expression = f"({a}x + {b}y)^2 - {a*a}x^2 - {b*b}y^2"
        steps = [
            f"Раскрываем скобки: {a*a}x² + 2·{a}·{b}xy + {b*b}y²",
            f"Вычитаем {a*a}x² и {b*b}y²",
            f"Остаётся: 2·{a}·{b}xy = {2*a*b}xy"
        ]
        topic_used = topic or "фсу"
    
    task = Task(
        level=level,
        sub_level=sub_level,
        topic=topic_used,
        expression=expression,
        answer=str(answer),
        solution_steps=steps,
        difficulty=level * 10 + sub_level,
        is_ai_generated=False
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    
    return task


async def _generate_ai_task(
    level: int,
    sub_level: int,
    topic: Optional[str],
    db: AsyncSession
) -> Task:
    """Generate task using AI for complex levels."""
    # Placeholder - would call OpenRouter API
    # For now, create a sample task
    task = Task(
        level=level,
        sub_level=sub_level,
        topic=topic or LEVELS[level - 1].topics[0],
        expression="\\text{AI-generated task placeholder}",
        answer="42",
        solution_steps=["AI generation not yet implemented"],
        difficulty=level * 10 + sub_level,
        is_ai_generated=True
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    
    return task


@router.post("/validate", response_model=TaskValidateResponse)
async def validate_answer(
    request: TaskValidateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Validate user answer and record session."""
    # Get task
    result = await db.execute(select(Task).where(Task.id == request.task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Validate answer
    is_correct = _compare_answers(request.user_answer, task.answer)
    
    # Calculate XP
    base_xp = task.level * 10
    if is_correct:
        # Bonus for mental steps
        mental_bonus = request.mental_steps * 2
        # Penalty for hints
        hint_penalty = request.hints_used * 5
        xp_earned = max(1, base_xp + mental_bonus - hint_penalty)
    else:
        xp_earned = 0
    
    # Record session
    session = TaskSession(
        user_id=current_user.id,
        task_id=task.id,
        user_answer=request.user_answer,
        is_correct=is_correct,
        mental_steps=request.mental_steps,
        written_steps=request.written_steps,
        time_seconds=request.time_seconds,
        xp_earned=xp_earned,
        hints_used=request.hints_used
    )
    db.add(session)
    
    # Update progress
    result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == current_user.id)
    )
    progress = result.scalar_one_or_none()
    if progress:
        progress.total_tasks += 1
        progress.total_xp += xp_earned
        progress.last_activity = datetime.utcnow()
        if is_correct:
            progress.correct_tasks += 1
            # Level up logic
            if progress.level_progress >= 100:
                progress.current_level = min(10, progress.current_level + 1)
                progress.level_progress = 0
            else:
                progress.level_progress += task.level * 5
    
    await db.commit()
    
    return TaskValidateResponse(
        is_correct=is_correct,
        correct_answer=task.answer,
        xp_earned=xp_earned,
        solution_steps=task.solution_steps
    )


def _compare_answers(user_answer: str, correct_answer: str) -> bool:
    """Compare user answer with correct answer."""
    # Normalize
    user = user_answer.strip().lower().replace(" ", "").replace("\\", "")
    correct = correct_answer.strip().lower().replace(" ", "").replace("\\", "")
    
    # Direct match
    if user == correct:
        return True
    
    # Numeric comparison
    try:
        user_num = float(user.replace(",", "."))
        correct_num = float(correct.replace(",", "."))
        return abs(user_num - correct_num) < 0.001
    except ValueError:
        pass
    
    return False
