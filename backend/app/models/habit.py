from datetime import date

from pydantic import BaseModel, Field


class HabitProgress(BaseModel):
    """Daily completion record for a habit."""

    day: date
    completed: bool = False


class Habit(BaseModel):
    """Habit metadata and completion tracking."""

    name: str = Field(..., min_length=1, max_length=120)
    frequency: str = Field(default="daily", description="daily, weekly, custom")
    progress: list[HabitProgress] = Field(default_factory=list)
