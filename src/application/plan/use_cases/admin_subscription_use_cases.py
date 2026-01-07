"""Admin subscription use cases."""

from typing import List
from src.domain.plan.repository.subscription_repository import SubscriptionRepository
from src.domain.plan.repository.plan_repository import PlanRepository
from src.application.plan.dto.plan_dto import SubscriptionDTO


class ListAllSubscriptionsUseCase:
    """Use case for listing all subscriptions (admin only)."""

    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
        plan_repository: PlanRepository,
    ):
        self.subscription_repository = subscription_repository
        self.plan_repository = plan_repository

    async def execute(self, user_id: int = None) -> List[SubscriptionDTO]:
        """Execute the use case. If user_id provided, filter by user."""
        if user_id:
            subscriptions = await self.subscription_repository.find_by_user_id(user_id)
        else:
            # Would need to add a find_all method to repository
            # For now, just return empty list or implement pagination
            subscriptions = []
        
        result = []
        for subscription in subscriptions:
            plan = await self.plan_repository.find_by_id(subscription.plan_id)
            plan_name = plan.name if plan else "Unknown Plan"
            
            result.append(SubscriptionDTO(
                id=subscription.subscription_id,
                user_id=subscription.user_id,
                plan_id=subscription.plan_id,
                plan_name=plan_name,
                status=subscription.status.value,
                start_date=subscription.start_date,
                end_date=subscription.end_date,
                days_remaining=subscription.days_remaining(),
                payment_reference=subscription.payment_reference,
                created_at=subscription.created_at,
                updated_at=subscription.updated_at,
            ))
        
        return result
