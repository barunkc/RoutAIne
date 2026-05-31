from datetime import date

from pydantic import BaseModel, Field

from app.models.routine import RoutineSlot


class Schedule(BaseModel):
    """Daily schedule composed of routine time blocks."""

    day: date
    blocks: list[RoutineSlot] = Field(default_factory=list)
