"""NotificationRepository implementation - PostgreSQL persistence."""

from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.notification.entities.notification import Notification
from src.domain.notification.repository.notification_repository import NotificationRepository
from src.infrastructure.persistence.models.notification import NotificationModel


class PostgreSQLNotificationRepository(NotificationRepository):
    """SQLAlchemy-based NotificationRepository for PostgreSQL."""

    def __init__(self, db_session: Session):
        """Initialize repository with database session."""
        self._session = db_session

    def find_by_user_id(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        unread_only: bool = False
    ) -> List[Notification]:
        """Find notifications for a user."""
        query = self._session.query(NotificationModel).filter(
            NotificationModel.user_id == user_id
        )
        
        if unread_only:
            query = query.filter(NotificationModel.is_read == False)
        
        models = query.order_by(NotificationModel.created_at.desc()).offset(skip).limit(limit).all()
        return [self._to_entity(model) for model in models]

    def find_by_id(self, notification_id: int) -> Optional[Notification]:
        """Find a notification by ID."""
        model = self._session.query(NotificationModel).filter(
            NotificationModel.id == notification_id
        ).first()
        return self._to_entity(model) if model else None

    def create(self, notification: Notification) -> Notification:
        """Create a new notification."""
        model = NotificationModel(
            user_id=notification.user_id,
            title=notification.title,
            message=notification.message,
            notification_type=notification.notification_type,
            is_read=notification.is_read,
            related_id=notification.related_id,
        )
        self._session.add(model)
        self._session.flush()
        notification.notification_id = model.id
        self._session.commit()
        return notification

    def mark_as_read(self, notification_id: int) -> bool:
        """Mark a notification as read."""
        model = self._session.query(NotificationModel).filter(
            NotificationModel.id == notification_id
        ).first()
        
        if model:
            model.is_read = True
            self._session.commit()
            return True
        return False

    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all notifications as read for a user."""
        count = self._session.query(NotificationModel).filter(
            NotificationModel.user_id == user_id,
            NotificationModel.is_read == False
        ).update({"is_read": True})
        self._session.commit()
        return count

    def count_unread(self, user_id: int) -> int:
        """Count unread notifications for a user."""
        return self._session.query(NotificationModel).filter(
            NotificationModel.user_id == user_id,
            NotificationModel.is_read == False
        ).count()

    def _to_entity(self, model: NotificationModel) -> Notification:
        """Convert ORM model to domain entity."""
        return Notification(
            notification_id=model.id,
            user_id=model.user_id,
            title=model.title,
            message=model.message,
            notification_type=model.notification_type,
            is_read=model.is_read,
            related_id=model.related_id,
            created_at=model.created_at,
        )
