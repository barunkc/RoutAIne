"""
Schedule models for MongoDB.

Defines the schema for daily schedules.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ScheduleResponse(BaseModel):
    """Schedule response schema."""
    id: str = Field(alias="_id")
    date: datetime
    routineId: str
    totalTasks: int
    completedTasks: int
    totalDuration: int = Field(..., description="Total duration in minutes")
    createdAt: datetime
    updatedAt: datetime

    class Config:
        populate_by_name = True


class DayScheduleResponse(BaseModel):
    """Full day schedule with all details."""
    date: datetime
    timeBlocks: list[dict]
    summary: dict = Field(
        default_factory=lambda: {
            "totalTasks": 0,
            "totalDuration": 0,
            "completedTasks": 0,
            "upcomingTasks": []
        }
    )
