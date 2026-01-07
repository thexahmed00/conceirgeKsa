"""Notifications API endpoints."""

from fastapi import APIRouter, Depends, Query

from src.application.notification.dto.notification_dto import (
    NotificationListResponseDTO,
    MarkAsReadResponseDTO,
    UnreadCountResponseDTO,
)
from src.application.notification.use_cases.notification_use_cases import (
    GetUserNotificationsUseCase,
    MarkNotificationAsReadUseCase,
    MarkAllNotificationsAsReadUseCase,
    GetUnreadCountUseCase,
)
from src.infrastructure.web.dependencies import get_current_user
from src.infrastructure.persistence.repositories.notification_repository import PostgreSQLNotificationRepository
from src.infrastructure.web.dependencies import get_db
from sqlalchemy.orm import Session
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/notifications",
    tags=["notifications"],
)


# Dependency injection functions
def get_notification_repository(db: Session = Depends(get_db)) -> PostgreSQLNotificationRepository:
    """Get notification repository."""
    return PostgreSQLNotificationRepository(db)


def get_notifications_use_case(
    notification_repo: PostgreSQLNotificationRepository = Depends(get_notification_repository),
) -> GetUserNotificationsUseCase:
    """Get user notifications use case."""
    return GetUserNotificationsUseCase(notification_repo)


def get_mark_as_read_use_case(
    notification_repo: PostgreSQLNotificationRepository = Depends(get_notification_repository),
) -> MarkNotificationAsReadUseCase:
    """Get mark notification as read use case."""
    return MarkNotificationAsReadUseCase(notification_repo)


def get_mark_all_as_read_use_case(
    notification_repo: PostgreSQLNotificationRepository = Depends(get_notification_repository),
) -> MarkAllNotificationsAsReadUseCase:
    """Get mark all notifications as read use case."""
    return MarkAllNotificationsAsReadUseCase(notification_repo)


def get_unread_count_use_case(
    notification_repo: PostgreSQLNotificationRepository = Depends(get_notification_repository),
) -> GetUnreadCountUseCase:
    """Get unread count use case."""
    return GetUnreadCountUseCase(notification_repo)


@router.get("", response_model=NotificationListResponseDTO, summary="Get user notifications")
async def get_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    unread_only: bool = Query(False, description="Get only unread notifications"),
    user_id: int = Depends(get_current_user),
    use_case: GetUserNotificationsUseCase = Depends(get_notifications_use_case),
) -> NotificationListResponseDTO:
    """
    Get current user's notifications.
    
    Returns paginated list of notifications with unread count.
    """
    return use_case.execute(
        user_id=user_id,
        skip=skip,
        limit=limit,
        unread_only=unread_only
    )


@router.get("/unread-count", response_model=UnreadCountResponseDTO, summary="Get unread notification count")
async def get_unread_count(
    user_id: int = Depends(get_current_user),
    use_case: GetUnreadCountUseCase = Depends(get_unread_count_use_case),
) -> UnreadCountResponseDTO:
    """
    Get count of unread notifications for current user.
    """
    return use_case.execute(user_id)


@router.put("/{notification_id}/read", response_model=MarkAsReadResponseDTO, summary="Mark notification as read")
async def mark_as_read(
    notification_id: int,
    user_id: int = Depends(get_current_user),
    use_case: MarkNotificationAsReadUseCase = Depends(get_mark_as_read_use_case),
) -> MarkAsReadResponseDTO:
    """
    Mark a specific notification as read.
    """
    return use_case.execute(notification_id, user_id)


@router.put("/mark-all-read", response_model=MarkAsReadResponseDTO, summary="Mark all notifications as read")
async def mark_all_as_read(
    user_id: int = Depends(get_current_user),
    use_case: MarkAllNotificationsAsReadUseCase = Depends(get_mark_all_as_read_use_case),
) -> MarkAsReadResponseDTO:
    """
    Mark all notifications as read for current user.
    """
    return use_case.execute(user_id)
