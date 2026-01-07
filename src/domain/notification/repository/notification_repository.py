"""Notification repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.notification.entities.notification import Notification


class NotificationRepository(ABC):
    """Abstract repository for Notification entities."""

    @abstractmethod
    async def find_by_user_id(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        unread_only: bool = False
    ) -> List[Notification]:
        """Find notifications for a user."""
        pass

    @abstractmethod
    async def find_by_id(self, notification_id: int) -> Optional[Notification]:
        """Find a notification by ID."""
        pass

    @abstractmethod
    async def create(self, notification: Notification) -> Notification:
        """Create a new notification."""
        pass

    @abstractmethod
    async def mark_as_read(self, notification_id: int) -> bool:
        """Mark a notification as read."""
        pass

    @abstractmethod
    async def mark_all_as_read(self, user_id: int) -> int:
        """Mark all notifications as read for a user. Returns count of updated notifications."""
        pass

    @abstractmethod
    async def count_unread(self, user_id: int) -> int:
        """Count unread notifications for a user."""
        pass
