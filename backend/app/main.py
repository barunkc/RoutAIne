"""
RoutAIne Backend - Main Application Entry Point

FastAPI application initialization and configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db
from app.api import tasks, routines, schedules, habits, notifications


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifespan events.
    Startup: Initialize database connections
    Shutdown: Clean up resources
    """
    # Startup
    print("Starting RoutAIne backend...")
    await init_db()
    yield
    # Shutdown
    print("Shutting down RoutAIne backend...")


# Create FastAPI application
app = FastAPI(
    title="RoutAIne API",
    description="AI-powered adaptive planner and scheduler API",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(routines.router, prefix="/api/routines", tags=["routines"])
app.include_router(schedules.router, prefix="/api/schedules", tags=["schedules"])
app.include_router(habits.router, prefix="/api/habits", tags=["habits"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])


@app.get("/", tags=["health"])
async def root():
    """Root health check endpoint."""
    return {
        "name": "RoutAIne API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
