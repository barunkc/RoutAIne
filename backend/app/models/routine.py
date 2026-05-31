from datetime import datetime

from pydantic import BaseModel, Field


class RoutineSlot(BaseModel):
    """Single time allocation block in a generated routine."""

    task_title: str
    start_time: datetime
    end_time: datetime


class Routine(BaseModel):
    """AI-generated routine based on task priorities and constraints."""

    generated_at: datetime = Field(default_factory=datetime.utcnow)
    slots: list[RoutineSlot] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
