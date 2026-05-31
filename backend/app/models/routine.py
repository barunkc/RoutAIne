"""
Routine models for MongoDB.

Defines the schema for daily routines with time blocks.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class TimeBlockType(str, Enum):
    """Type of time block."""
    TASK = "task"
    BREAK = "break"
    HABIT = "habit"
    FREE = "free"


class RoutineType(str, Enum):
    """How routine was generated."""
    AI = "ai"
    MANUAL = "manual"


class TimeBlock(BaseModel):
    """Individual time block in a routine."""
    startTime: str = Field(..., description="Start time in HH:MM format")
    endTime: str = Field(..., description="End time in HH:MM format")
    taskId: Optional[str] = None
    title: str = Field(..., description="Title of the activity")
    type: TimeBlockType = TimeBlockType.TASK
    description: Optional[str] = None


class RoutineCreate(BaseModel):
    """Routine creation schema."""
    date: datetime
    timeBlocks: list[TimeBlock]
    generatedBy: RoutineType = RoutineType.MANUAL


class RoutineUpdate(BaseModel):
    """Routine update schema."""
    timeBlocks: Optional[list[TimeBlock]] = None


class RoutineResponse(BaseModel):
    """Routine response schema."""
    id: str = Field(alias="_id")
    date: datetime
    timeBlocks: list[TimeBlock]
    generatedBy: RoutineType
    aiScore: Optional[float] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        populate_by_name = True


class RoutineGenerateRequest(BaseModel):
    """Request to generate routine via AI."""
    date: datetime
    taskIds: list[str] = Field(..., description="Task IDs to include in routine")
    preferredStartTime: str = Field("09:00", description="Preferred start time in HH:MM format")
    preferredEndTime: str = Field("18:00", description="Preferred end time in HH:MM format")
    breakDurationMinutes: int = Field(15, description="Minutes for breaks between tasks")
