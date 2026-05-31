from datetime import datetime

from pydantic import BaseModel, Field


class Task(BaseModel):
    """Represents a user task to be planned into a routine."""

    title: str = Field(..., min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    duration: int = Field(..., ge=5, le=720, description="Task duration in minutes")
    priority: int = Field(default=3, ge=1, le=5)
    deadline: datetime | None = None
