from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import router as api_router
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    await init_db()
    yield
    # Shutdown


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title="Mental Math Trainer API",
        description="API for mental math training application",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API router
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    
    @app.get("/")
    async def root():
        return {"message": "Mental Math Trainer API", "version": "1.0.0"}
    
    @app.get("/health")
    async def health():
        return {"status": "ok"}
    
    return app


app = create_app()
