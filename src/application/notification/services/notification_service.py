"""Notification service for creating notifications throughout the application."""

from datetime import datetime
from sqlalchemy.orm import Session

from src.domain.notification.entities.notification import Notification, NotificationType
from src.infrastructure.persistence.repositories.notification_repository import PostgreSQLNotificationRepository


class NotificationService:
    """Service for creating and managing notifications."""

    def __init__(self, db_session: Session):
        """Initialize notification service with database session."""
        self.notification_repo = PostgreSQLNotificationRepository(db_session)

    def create_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: NotificationType,
        related_id: int = None,
    ) -> Notification:
        """
        Create a new notification for a user.
        
        Args:
            user_id: The user to notify
            title: Notification title
            message: Notification message
            notification_type: Type of notification
            related_id: Optional ID of related entity (booking, request, etc.)
            
        Returns:
            Created notification
        """
        notification = Notification(
            notification_id=0,  # Will be set by repository
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            is_read=False,
            related_id=related_id,
            created_at=datetime.utcnow(),
        )
        
        return self.notification_repo.create(notification)

    def notify_booking_confirmed(self, user_id: int, booking_id: int, booking_details: str):
        """Create notification for booking confirmation."""
        return self.create_notification(
            user_id=user_id,
            title="Booking Confirmed",
            message=f"Your booking has been confirmed. {booking_details}",
            notification_type=NotificationType.BOOKING_CONFIRMED,
            related_id=booking_id,
        )

    def notify_booking_cancelled(self, user_id: int, booking_id: int):
        """Create notification for booking cancellation."""
        return self.create_notification(
            user_id=user_id,
            title="Booking Cancelled",
            message="We regret to inform you that your booking has been cancelled. Please contact support if you have any questions.",
            notification_type=NotificationType.BOOKING_CANCELLED,
            related_id=booking_id,
        )

    def notify_request_updated(self, user_id: int, request_id: int, status: str):
        """Create notification for request status update."""
        return self.create_notification(
            user_id=user_id,
            title="Request Updated",
            message=f"Your request status has been updated to: {status}",
            notification_type=NotificationType.REQUEST_UPDATED,
            related_id=request_id,
        )

    def notify_message_received(self, user_id: int, conversation_id: int, sender_name: str):
        """Create notification for new message."""
        return self.create_notification(
            user_id=user_id,
            title="New Message",
            message=f"You received a new message from {sender_name}",
            notification_type=NotificationType.MESSAGE_RECEIVED,
            related_id=conversation_id,
        )

    def notify_subscription_activated(self, user_id: int, plan_name: str, subscription_id: int):
        """Create notification for subscription activation."""
        return self.create_notification(
            user_id=user_id,
            title="Subscription Activated",
            message=f"Your {plan_name} subscription has been activated!",
            notification_type=NotificationType.SUBSCRIPTION_ACTIVATED,
            related_id=subscription_id,
        )

    def notify_subscription_expiring(self, user_id: int, days_remaining: int, subscription_id: int):
        """Create notification for subscription expiring soon."""
        return self.create_notification(
            user_id=user_id,
            title="Subscription Expiring Soon",
            message=f"Your subscription will expire in {days_remaining} days. Renew now to continue enjoying our services.",
            notification_type=NotificationType.SUBSCRIPTION_EXPIRING,
            related_id=subscription_id,
        )

    def notify_general(self, user_id: int, title: str, message: str):
        """Create a general notification."""
        return self.create_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=NotificationType.GENERAL,
        )

    def notify_new_request(self, admin_user_id: int, request_id: int, request_title: str, user_name: str = None):
        """Create notification for admin about new request."""
        user_info = f" from {user_name}" if user_name else ""
        return self.create_notification(
            user_id=admin_user_id,
            title="New Request",
            message=f"New request{user_info}: {request_title}",
            notification_type=NotificationType.NEW_REQUEST,
            related_id=request_id,
        )


def get_notification_service(db: Session) -> NotificationService:
    """Get notification service instance."""
    return NotificationService(db)
