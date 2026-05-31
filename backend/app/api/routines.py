from fastapi import APIRouter

from app.models import Task
from app.services.ai_service import AIService

router = APIRouter(prefix="/routines", tags=["routines"])


@router.post("/generate")
async def generate_daily_routine() -> dict[str, object]:
    """Generate a routine from sample tasks until persistence is wired."""
    ai_service = AIService()
    routine = await ai_service.generate_routine(
        [
            Task(title="Deep work", duration=90, priority=1),
            Task(title="Admin", duration=30, priority=3),
        ]
    )

    return {
        "routine_id": routine.generated_at.isoformat(),
        "recommendations": routine.recommendations,
        "slots": [slot.model_dump(mode="json") for slot in routine.slots],
    }
