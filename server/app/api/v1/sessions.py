from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.models import TaskSession, User, UserProgress
from app.schemas.session import TaskSessionRead, SessionStats, ProgressResponse
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/sessions", tags=["sessions"])
progress_router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/", response_model=List[TaskSessionRead])
async def list_sessions(
    limit: int = Query(20, le=100),
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List user's task sessions."""
    query = (
        select(TaskSession)
        .where(TaskSession.user_id == current_user.id)
        .order_by(TaskSession.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/stats", response_model=SessionStats)
async def get_session_stats(
    days: int = Query(7, le=30),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get session statistics for the last N days."""
    since = datetime.utcnow() - timedelta(days=days)
    
    # Count totals
    query = (
        select(
            func.count(TaskSession.id).label("total"),
            func.sum(TaskSession.xp_earned).label("xp"),
            func.avg(TaskSession.time_seconds).label("avg_time")
        )
        .where(TaskSession.user_id == current_user.id)
        .where(TaskSession.created_at >= since)
    )
    result = await db.execute(query)
    row = result.one()
    
    total_sessions = row.total or 0
    total_xp = row.xp or 0
    avg_time = row.avg_time or 0
    
    # Count correct
    query = (
        select(func.count(TaskSession.id))
        .where(TaskSession.user_id == current_user.id)
        .where(TaskSession.created_at >= since)
        .where(TaskSession.is_correct == True)
    )
    result = await db.execute(query)
    correct_sessions = result.scalar() or 0
    
    accuracy = (correct_sessions / total_sessions * 100) if total_sessions > 0 else 0
    
    return SessionStats(
        total_sessions=total_sessions,
        correct_sessions=correct_sessions,
        total_xp=total_xp,
        avg_time_seconds=avg_time,
        accuracy=accuracy
    )


@progress_router.get("/", response_model=ProgressResponse)
async def get_progress(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user progress."""
    result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == current_user.id)
    )
    progress = result.scalar_one_or_none()
    
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    accuracy = (progress.correct_tasks / progress.total_tasks * 100) if progress.total_tasks > 0 else 0
    
    # XP needed for next level (simple formula)
    next_level_xp = progress.current_level * 100
    
    return ProgressResponse(
        current_level=progress.current_level,
        current_sub_level=progress.current_sub_level,
        level_progress=progress.level_progress,
        total_xp=progress.total_xp,
        total_tasks=progress.total_tasks,
        correct_tasks=progress.correct_tasks,
        streak_days=progress.streak_days,
        accuracy=accuracy,
        next_level_xp=next_level_xp
    )
