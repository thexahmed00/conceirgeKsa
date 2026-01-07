"""Notification domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class NotificationType(str, Enum):
    """Notification type enum."""
    BOOKING_CONFIRMED = "booking_confirmed"
    BOOKING_CANCELLED = "booking_cancelled"
    REQUEST_UPDATED = "request_updated"
    NEW_REQUEST = "new_request"
    MESSAGE_RECEIVED = "message_received"
    SUBSCRIPTION_ACTIVATED = "subscription_activated"
    SUBSCRIPTION_EXPIRING = "subscription_expiring"
    GENERAL = "general"


@dataclass
class Notification:
    """
    Notification entity represents a notification sent to a user.
    """
    notification_id: int
    user_id: int
    title: str
    message: str
    notification_type: NotificationType
    is_read: bool = False
    related_id: Optional[int] = None  # Related entity ID (booking, request, etc.)
    created_at: Optional[datetime] = None

    def mark_as_read(self):
        """Mark notification as read."""
        self.is_read = True
