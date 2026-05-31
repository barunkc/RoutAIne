import asyncio
import logging

from fastapi import FastAPI

from app.api import api_router
from app.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(api_router)
logger = logging.getLogger(__name__)
_background_tasks: list[asyncio.Task[None]] = []


async def _sms_notification_worker() -> None:
    """Placeholder SMS worker loop for hosted or always-on execution."""
    while True:
        await asyncio.sleep(settings.sms_worker_interval_seconds)
        logger.debug("SMS worker heartbeat")


async def _scheduled_routine_generator() -> None:
    """Placeholder routine scheduler loop for periodic routine generation."""
    while True:
        await asyncio.sleep(settings.routine_generator_interval_seconds)
        logger.debug("Routine generator heartbeat")


async def _habit_tracker_worker() -> None:
    """Placeholder habit tracker loop for periodic habit updates."""
    while True:
        await asyncio.sleep(settings.habit_tracker_interval_seconds)
        logger.debug("Habit tracker heartbeat")


@app.on_event("startup")
async def startup_event() -> None:
    # Spawn background workers so SMS/routine/habit tasks can run while service is up.
    _background_tasks.extend(
        [
            asyncio.create_task(_sms_notification_worker()),
            asyncio.create_task(_scheduled_routine_generator()),
            asyncio.create_task(_habit_tracker_worker()),
        ]
    )


@app.on_event("shutdown")
async def shutdown_event() -> None:
    # Gracefully stop worker loops.
    for task in _background_tasks:
        task.cancel()

    await asyncio.gather(*_background_tasks, return_exceptions=True)
    _background_tasks.clear()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
