"""
Notification models for MongoDB.

Defines the schema for SMS and in-app notifications.
"""

from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum


class NotificationStatus(str, Enum):
    """Notification status."""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    DELIVERED = "delivered"


class NotificationType(str, Enum):
    """Type of notification."""
    SMS = "sms"
    EMAIL = "email"
    IN_APP = "in_app"


class SMSNotificationCreate(BaseModel):
    """SMS notification creation schema."""
    recipientPhone: str = Field(..., description="E.164 format phone number")
    message: str = Field(..., max_length=160, description="SMS message content")
    taskId: Optional[str] = None
    habitId: Optional[str] = None
    scheduledTime: Optional[datetime] = None


class NotificationResponse(BaseModel):
    """Notification response schema."""
    id: str = Field(alias="_id")
    type: NotificationType
    recipientPhone: Optional[str] = None
    message: str
    taskId: Optional[str] = None
    habitId: Optional[str] = None
    status: NotificationStatus
    sentAt: datetime
    deliveredAt: Optional[datetime] = None
    retryCount: int = 0
    lastRetryAt: Optional[datetime] = None
    errorMessage: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        populate_by_name = True


class NotificationHistoryResponse(BaseModel):
    """Notification history response."""
    totalNotifications: int
    sentNotifications: int
    failedNotifications: int
    pendingNotifications: int
    notifications: list[NotificationResponse]
