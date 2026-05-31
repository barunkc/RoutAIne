from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.database import get_database
from app.models import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=Task)
async def create_task(task: Task) -> Task:
    """Create a task document in MongoDB."""
    db = get_database()
    payload = task.model_dump(mode="json")

    if payload.get("deadline") and isinstance(payload["deadline"], str):
        payload["deadline"] = datetime.fromisoformat(payload["deadline"])

    result = await db.tasks.insert_one(payload)
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to persist task")

    return task


@router.get("", response_model=list[Task])
async def list_tasks() -> list[Task]:
    """List all tasks from MongoDB."""
    db = get_database()
    tasks = await db.tasks.find().to_list(length=500)
    return [Task(**task) for task in tasks]
