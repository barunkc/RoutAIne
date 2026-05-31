from fastapi import APIRouter

from app.services.habit_service import HabitService

router = APIRouter(prefix="/habits", tags=["habits"])


@router.get("")
async def list_habits() -> list[dict[str, object]]:
    """Return current habit tracking records."""
    habits = await HabitService().list_habits()
    return [habit.model_dump(mode="json") for habit in habits]
