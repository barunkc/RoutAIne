from datetime import datetime

from pydantic import BaseModel, Field


class Notification(BaseModel):
    """Tracks SMS notification sends and delivery state."""

    message: str = Field(..., min_length=1, max_length=500)
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="queued")
    recipient: str | None = None
