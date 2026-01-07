"""Background task to check for expiring subscriptions."""

import asyncio
from datetime import datetime
from typing import List

from src.infrastructure.persistence.database import SessionLocal
from src.infrastructure.persistence.repositories.plan.plan_repository import PostgreSQLPlanRepository
from src.infrastructure.persistence.repositories.plan.subscription_repository import PostgreSQLSubscriptionRepository
from src.infrastructure.persistence.repositories.notification_repository import PostgreSQLNotificationRepository
from src.application.notification.services.notification_service import NotificationService
from src.domain.plan.entities.subscription import SubscriptionStatus
from src.shared.logger.config import get_logger

logger = get_logger(__name__)


def check_expiring_subscriptions() -> int:
    """
    Check for subscriptions expiring in 3 days and send notifications.
    
    Returns:
        Number of notifications sent
    """
    db = SessionLocal()
    notifications_sent = 0
    
    try:
        # Initialize repositories
        subscription_repo = PostgreSQLSubscriptionRepository(db)
        plan_repo = PostgreSQLPlanRepository(db)
        notification_repo = PostgreSQLNotificationRepository(db)
        notification_service = NotificationService(notification_repo)
        
        # Get all active subscriptions
        all_subscriptions = subscription_repo.list_all()
        
        logger.info(f"Checking {len(all_subscriptions)} subscriptions for expiration")
        
        for subscription in all_subscriptions:
            if subscription.status != SubscriptionStatus.ACTIVE:
                continue
                
            # Check days remaining
            days_left = subscription.days_remaining()
            
            # Notify if expiring in 3 days or less
            if days_left is not None and 0 < days_left <= 3:
                try:
                    plan = plan_repo.find_by_id(subscription.plan_id)
                    if plan:
                        notification_service.notify_subscription_expiring(
                            user_id=subscription.user_id,
                            plan_name=plan.name,
                            days_remaining=days_left,
                        )
                        notifications_sent += 1
                        logger.info(
                            f"Sent expiration notification to user {subscription.user_id} "
                            f"for plan {plan.name} ({days_left} days remaining)"
                        )
                except Exception as e:
                    logger.error(
                        f"Failed to send expiration notification for subscription "
                        f"{subscription.subscription_id}: {e}"
                    )
            
            # Auto-expire if past end date
            elif days_left is not None and days_left <= 0:
                try:
                    subscription.status = SubscriptionStatus.EXPIRED
                    subscription_repo.update(subscription)
                    logger.info(f"Auto-expired subscription {subscription.subscription_id}")
                except Exception as e:
                    logger.error(f"Failed to expire subscription {subscription.subscription_id}: {e}")
        
        logger.info(f"Subscription check complete. Sent {notifications_sent} notifications")
        return notifications_sent
        
    except Exception as e:
        logger.error(f"Error in subscription checker: {e}")
        return 0
    finally:
        db.close()


def run_subscription_checker():
    """Synchronous wrapper to run the subscription checker."""
    return check_expiring_subscriptions()


if __name__ == "__main__":
    # Can be run directly for testing
    print("Running subscription expiration checker...")
    count = run_subscription_checker()
    print(f"Complete. Sent {count} notifications.")
