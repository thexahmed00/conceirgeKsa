"""SQLAlchemy Notification model."""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean,
    ForeignKey, Index, Enum as SQLEnum
)
from src.infrastructure.persistence.models.user import Base
from src.domain.notification.entities.notification import NotificationType


class NotificationModel(Base):
    """SQLAlchemy model for notifications."""
    
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(
        SQLEnum(NotificationType, name='notification_type'),
        nullable=False,
        default=NotificationType.GENERAL
    )
    
    is_read = Column(Boolean, nullable=False, default=False)
    related_id = Column(Integer, nullable=True)  # Generic reference to related entity
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        Index('idx_notification_user', 'user_id'),
        Index('idx_notification_unread', 'user_id', 'is_read'),
        Index('idx_notification_created', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<NotificationModel(id={self.id}, user_id={self.user_id}, type={self.notification_type})>"
