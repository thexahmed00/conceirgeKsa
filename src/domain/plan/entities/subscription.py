"""Subscription domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class SubscriptionStatus(str, Enum):
    """Subscription status enum."""
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    PENDING = "pending"  # Awaiting payment verification


@dataclass
class Subscription:
    """
    Subscription entity represents a user's subscription to a plan.
    """
    subscription_id: int
    user_id: int
    plan_id: int
    status: SubscriptionStatus
    start_date: datetime
    end_date: datetime
    payment_reference: Optional[str] = None  # Payment gateway reference
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_active(self) -> bool:
        """Check if subscription is currently active."""
        now = datetime.utcnow()
        return (
            self.status == SubscriptionStatus.ACTIVE 
            and self.start_date <= now <= self.end_date
        )

    def days_remaining(self) -> int:
        """Calculate days remaining in subscription."""
        if not self.is_active():
            return 0
        delta = self.end_date - datetime.utcnow()
        return max(0, delta.days)
