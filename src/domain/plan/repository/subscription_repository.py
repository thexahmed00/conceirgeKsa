"""Subscription repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.plan.entities.subscription import Subscription, SubscriptionStatus


class SubscriptionRepository(ABC):
    """Abstract repository for Subscription entities."""

    @abstractmethod
    async def find_by_id(self, subscription_id: int) -> Optional[Subscription]:
        """Find a subscription by ID."""
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: int) -> List[Subscription]:
        """Find all subscriptions for a user."""
        pass

    @abstractmethod
    async def find_active_by_user_id(self, user_id: int) -> Optional[Subscription]:
        """Find the active subscription for a user."""
        pass

    @abstractmethod
    async def create(self, subscription: Subscription) -> Subscription:
        """Create a new subscription."""
        pass

    @abstractmethod
    async def update(self, subscription: Subscription) -> Subscription:
        """Update an existing subscription."""
        pass

    @abstractmethod
    async def find_by_payment_reference(self, payment_reference: str) -> Optional[Subscription]:
        """Find a subscription by payment reference."""
        pass
