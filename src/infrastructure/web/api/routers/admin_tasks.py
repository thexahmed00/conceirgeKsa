"""Admin endpoints for managing background tasks."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.infrastructure.tasks.subscription_checker import run_subscription_checker
from src.infrastructure.tasks.scheduler import get_scheduler_status
from src.infrastructure.web.dependencies import get_current_admin_user
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/admin/tasks",
    tags=["admin-tasks"],
)


class TaskStatusResponse(BaseModel):
    """Response model for scheduler status."""
    running: bool
    jobs: list


class SubscriptionCheckResponse(BaseModel):
    """Response model for subscription checker."""
    success: bool
    notifications_sent: int
    message: str


@router.get("/status", response_model=TaskStatusResponse)
async def get_tasks_status(
    admin_id: int = Depends(get_current_admin_user),
) -> TaskStatusResponse:
    """Get the status of background scheduler and all scheduled jobs (admin only)."""
    status = get_scheduler_status()
    logger.info(f"Admin {admin_id} checked task status")
    return TaskStatusResponse(**status)


@router.post("/subscription-checker/run", response_model=SubscriptionCheckResponse)
async def trigger_subscription_checker(
    admin_id: int = Depends(get_current_admin_user),
) -> SubscriptionCheckResponse:
    """Manually trigger the subscription expiration checker (admin only)."""
    try:
        count = run_subscription_checker()
        logger.info(f"Admin {admin_id} manually triggered subscription checker. Sent {count} notifications")
        
        return SubscriptionCheckResponse(
            success=True,
            notifications_sent=count,
            message=f"Subscription checker completed. Sent {count} expiration notifications.",
        )
    except Exception as e:
        logger.error(f"Error running subscription checker: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to run subscription checker: {str(e)}")
