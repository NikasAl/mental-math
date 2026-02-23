from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    account_key = Column(String(64), unique=True, index=True, nullable=False)
    nickname = Column(String(50), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    progress = relationship("UserProgress", back_populates="user", uselist=False)
    sessions = relationship("TaskSession", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    current_level = Column(Integer, default=1)
    current_sub_level = Column(Integer, default=1)
    level_progress = Column(Integer, default=0)  # 0-100 for current level
    total_xp = Column(Integer, default=0)
    total_tasks = Column(Integer, default=0)
    correct_tasks = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    last_activity = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="progress")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer, nullable=False)
    sub_level = Column(Integer, default=1)
    topic = Column(String(100), nullable=False)
    expression = Column(Text, nullable=False)  # LaTeX expression
    answer = Column(Text, nullable=False)
    solution_steps = Column(JSON, default=list)  # List of steps
    hint = Column(Text, nullable=True)
    difficulty = Column(Integer, default=0)
    is_ai_generated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sessions = relationship("TaskSession", back_populates="task")


class TaskSession(Base):
    __tablename__ = "task_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, default=False)
    mental_steps = Column(Integer, default=0)  # Number of mental steps used
    written_steps = Column(Integer, default=0)  # Number of written steps
    time_seconds = Column(Integer, default=0)
    xp_earned = Column(Integer, default=0)
    hints_used = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    task = relationship("Task", back_populates="sessions")


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)
    xp_reward = Column(Integer, default=0)
    condition_type = Column(String(50), nullable=False)  # e.g., "tasks_solved", "streak"
    condition_value = Column(Integer, default=0)


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    earned_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement")


class DailyChallenge(Base):
    __tablename__ = "daily_challenges"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, index=True)
    level = Column(Integer, nullable=False)
    task_ids = Column(JSON, default=list)  # List of task IDs
    created_at = Column(DateTime, default=datetime.utcnow)
