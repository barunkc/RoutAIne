from fastapi import APIRouter

from app.models import Task
from app.services.scheduler_service import SchedulerService

router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.get("")
async def get_today_schedule() -> dict[str, object]:
    """Get a generated schedule for today."""
    scheduler = SchedulerService()
    schedule = await scheduler.create_schedule(
        [
            Task(title="Deep work", duration=120, priority=1),
            Task(title="Workout", duration=45, priority=2),
        ]
    )

    return schedule.model_dump(mode="json")
