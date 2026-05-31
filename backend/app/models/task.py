"""
Task models for MongoDB.

Defines the schema for tasks with title, description, duration, priority, etc.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class PriorityLevel(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskCreate(BaseModel):
    """Task creation schema."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    duration: int = Field(..., gt=0, description="Duration in minutes")
    priority: PriorityLevel = PriorityLevel.MEDIUM
    deadline: Optional[datetime] = None
    category: str = Field("General", max_length=100)
    tags: list[str] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    """Task update schema."""
    title: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    priority: Optional[PriorityLevel] = None
    deadline: Optional[datetime] = None
    category: Optional[str] = None
    tags: Optional[list[str]] = None


class TaskResponse(BaseModel):
    """Task response schema."""
    id: str = Field(alias="_id")
    title: str
    description: Optional[str]
    duration: int
    priority: PriorityLevel
    deadline: Optional[datetime]
    category: str
    tags: list[str]
    createdAt: datetime
    updatedAt: datetime

    class Config:
        populate_by_name = True
