from fastapi import APIRouter

from app.api.v1 import auth, tasks, sessions

router = APIRouter()

router.include_router(auth.router)
router.include_router(tasks.router)
router.include_router(sessions.router)
router.include_router(sessions.progress_router)
