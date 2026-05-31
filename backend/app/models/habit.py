"""
Habit models for MongoDB.

Defines the schema for habit tracking with completion history.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class HabitFrequency(str, Enum):
    """Habit frequency options."""
    DAILY = "daily"
    WEEKLY = "weekly"
    CUSTOM = "custom"


class CompletionRecord(BaseModel):
    """Habit completion record."""
    date: datetime
    completed: bool
    notes: Optional[str] = None


class HabitCreate(BaseModel):
    """Habit creation schema."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    frequency: HabitFrequency = HabitFrequency.DAILY
    targetDays: Optional[list[int]] = Field(None, description="Days of week (0-6) for weekly habits")
    category: str = Field("Health", max_length=100)
    icon: Optional[str] = None


class HabitUpdate(BaseModel):
    """Habit update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[HabitFrequency] = None
    targetDays: Optional[list[int]] = None
    category: Optional[str] = None


class HabitResponse(BaseModel):
    """Habit response schema."""
    id: str = Field(alias="_id")
    name: str
    description: Optional[str]
    frequency: HabitFrequency
    targetDays: Optional[list[int]]
    category: str
    icon: Optional[str]
    completionHistory: list[CompletionRecord] = Field(default_factory=list)
    streak: int = 0
    bestStreak: int = 0
    totalCompleted: int = 0
    createdAt: datetime
    updatedAt: datetime

    class Config:
        populate_by_name = True


class HabitCompleteRequest(BaseModel):
    """Request to mark habit as completed."""
    date: datetime
    notes: Optional[str] = None
