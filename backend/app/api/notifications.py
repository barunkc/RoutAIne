from pydantic import BaseModel, Field
from fastapi import APIRouter

from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])


class SendSMSRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)
    recipient: str | None = None


@router.post("/send-sms")
async def send_sms_notification(payload: SendSMSRequest) -> dict[str, str | None]:
    """Send an SMS notification via Twilio, or queue if credentials are missing."""
    notification = await NotificationService().send_sms(payload.message, payload.recipient)
    return notification.model_dump(mode="json")
