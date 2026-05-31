"""
Notifications API routes.

Endpoints for managing SMS and email notifications.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
from bson import ObjectId

from app.database import get_db
from app.models.notification import SMSNotificationCreate, NotificationResponse, NotificationHistoryResponse
from app.services.notification_service import NotificationService

router = APIRouter()
notification_service = NotificationService()


@router.post("/send-sms", response_model=NotificationResponse, status_code=201)
async def send_sms_notification(request: SMSNotificationCreate):
    """
    Send an SMS notification.
    
    Args:
        request: SMS notification request with phone number and message
        
    Returns:
        Created notification record
    """
    db = await get_db()
    
    # Send SMS via Twilio
    success = await notification_service.send_sms(
        phone_number=request.recipientPhone,
        message=request.message
    )
    
    # Store notification record
    notification_data = {
        "type": "sms",
        "recipientPhone": request.recipientPhone,
        "message": request.message,
        "taskId": request.taskId,
        "habitId": request.habitId,
        "status": "sent" if success else "failed",
        "sentAt": datetime.utcnow(),
        "deliveredAt": datetime.utcnow() if success else None,
        "retryCount": 0,
        "errorMessage": None if success else "SMS sending failed",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }
    
    result = await db.notifications.insert_one(notification_data)
    
    created_notification = await db.notifications.find_one({"_id": result.inserted_id})
    return NotificationResponse(**created_notification)


@router.get("", response_model=NotificationHistoryResponse)
async def list_notifications(
    status: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """
    List notifications with statistics.
    
    Args:
        status: Filter by notification status
        skip: Number of notifications to skip
        limit: Maximum number of notifications to return
        
    Returns:
        Notification history with statistics
    """
    db = await get_db()
    
    query = {}
    if status:
        query["status"] = status
    
    notifications = await db.notifications.find(query).skip(skip).limit(limit).to_list(length=limit)
    
    # Get statistics
    all_notifications = await db.notifications.find(query).to_list(length=None)
    total_count = len(all_notifications)
    sent_count = len([n for n in all_notifications if n.get("status") == "sent"])
    failed_count = len([n for n in all_notifications if n.get("status") == "failed"])
    pending_count = len([n for n in all_notifications if n.get("status") == "pending"])
    
    return NotificationHistoryResponse(
        totalNotifications=total_count,
        sentNotifications=sent_count,
        failedNotifications=failed_count,
        pendingNotifications=pending_count,
        notifications=[NotificationResponse(**n) for n in notifications]
    )


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(notification_id: str):
    """
    Get a specific notification by ID.
    
    Args:
        notification_id: Notification ID
        
    Returns:
        Notification details
    """
    db = await get_db()
    
    try:
        notification = await db.notifications.find_one({"_id": ObjectId(notification_id)})
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        return NotificationResponse(**notification)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{notification_id}", status_code=204)
async def delete_notification(notification_id: str):
    """
    Delete a notification record.
    
    Args:
        notification_id: Notification ID
    """
    db = await get_db()
    
    try:
        result = await db.notifications.delete_one({"_id": ObjectId(notification_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Notification not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
