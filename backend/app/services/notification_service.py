from twilio.rest import Client

from app.config import settings
from app.models import Notification


class NotificationService:
    """Sends SMS notifications and records send metadata."""

    def __init__(self) -> None:
        self._client: Client | None = None
        if settings.twilio_account_sid and settings.twilio_auth_token:
            self._client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

    async def send_sms(self, message: str, to_number: str | None = None) -> Notification:
        recipient = to_number or settings.twilio_to_number

        if self._client and settings.twilio_from_number and recipient:
            twilio_message = self._client.messages.create(
                body=message,
                from_=settings.twilio_from_number,
                to=recipient,
            )
            return Notification(
                message=message,
                recipient=recipient,
                status=twilio_message.status or "queued",
            )

        return Notification(message=message, recipient=recipient, status="queued")
