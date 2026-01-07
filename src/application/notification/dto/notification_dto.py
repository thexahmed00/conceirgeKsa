"""Notification DTOs."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class NotificationDTO(BaseModel):
    """DTO for a notification."""
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    is_read: bool
    related_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponseDTO(BaseModel):
    """DTO for list of notifications."""
    notifications: List[NotificationDTO]
    total: int
    unread_count: int


class MarkAsReadResponseDTO(BaseModel):
    """DTO for mark as read response."""
    success: bool
    message: str


class UnreadCountResponseDTO(BaseModel):
    """DTO for unread count."""
    unread_count: int
