"""Notification use cases."""

from src.domain.notification.repository.notification_repository import NotificationRepository
from src.application.notification.dto.notification_dto import (
    NotificationDTO,
    NotificationListResponseDTO,
    MarkAsReadResponseDTO,
    UnreadCountResponseDTO,
)


class GetUserNotificationsUseCase:
    """Use case for getting user notifications."""

    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository

    def execute(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        unread_only: bool = False
    ) -> NotificationListResponseDTO:
        """Execute the use case."""
        notifications = self.notification_repository.find_by_user_id(
            user_id=user_id,
            skip=skip,
            limit=limit,
            unread_only=unread_only
        )
        
        unread_count = self.notification_repository.count_unread(user_id)
        
        notification_dtos = [
            NotificationDTO(
                id=n.notification_id,
                user_id=n.user_id,
                title=n.title,
                message=n.message,
                notification_type=n.notification_type.value,
                is_read=n.is_read,
                related_id=n.related_id,
                created_at=n.created_at,
            )
            for n in notifications
        ]
        
        return NotificationListResponseDTO(
            notifications=notification_dtos,
            total=len(notification_dtos),
            unread_count=unread_count,
        )


class MarkNotificationAsReadUseCase:
    """Use case for marking a notification as read."""

    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository

    def execute(self, notification_id: int, user_id: int) -> MarkAsReadResponseDTO:
        """Execute the use case."""
        # Verify notification belongs to user
        notification = self.notification_repository.find_by_id(notification_id)
        if not notification:
            return MarkAsReadResponseDTO(
                success=False,
                message="Notification not found"
            )
        
        if notification.user_id != user_id:
            return MarkAsReadResponseDTO(
                success=False,
                message="Unauthorized"
            )
        
        success = self.notification_repository.mark_as_read(notification_id)
        
        return MarkAsReadResponseDTO(
            success=success,
            message="Notification marked as read" if success else "Failed to mark as read"
        )


class MarkAllNotificationsAsReadUseCase:
    """Use case for marking all notifications as read."""

    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository

    def execute(self, user_id: int) -> MarkAsReadResponseDTO:
        """Execute the use case."""
        count = self.notification_repository.mark_all_as_read(user_id)
        
        return MarkAsReadResponseDTO(
            success=True,
            message=f"Marked {count} notifications as read"
        )


class GetUnreadCountUseCase:
    """Use case for getting unread notification count."""

    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository

    def execute(self, user_id: int) -> UnreadCountResponseDTO:
        """Execute the use case."""
        unread_count = self.notification_repository.count_unread(user_id)
        
        return UnreadCountResponseDTO(unread_count=unread_count)
