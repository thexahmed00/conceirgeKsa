"""Plan use cases."""

import json
from datetime import datetime, timedelta
from typing import List, Optional

from src.domain.plan.entities.plan import Plan
from src.domain.plan.entities.subscription import Subscription, SubscriptionStatus
from src.domain.plan.repository.plan_repository import PlanRepository
from src.domain.plan.repository.subscription_repository import SubscriptionRepository
from src.domain.user.repository.user_repository import UserRepository
from src.domain.shared.exceptions import ResourceNotFoundError
from src.application.plan.dto.plan_dto import (
    PlanDTO,
    PlanListResponseDTO,
    SubscriptionDTO,
    PurchasePlanRequestDTO,
    PurchasePlanResponseDTO,
    VerifyPaymentRequestDTO,
    VerifyPaymentResponseDTO,
)


class ListPlansUseCase:
    """Use case for listing available plans."""

    def __init__(self, plan_repository: PlanRepository):
        self.plan_repository = plan_repository

    def execute(self) -> PlanListResponseDTO:
        """Execute the use case."""
        plans = self.plan_repository.find_all(active_only=True)
        
        plan_dtos = []
        for plan in plans:
            # Parse features JSON if exists
            features = None
            if plan.features:
                try:
                    features = json.loads(plan.features)
                except:
                    features = []
            
            plan_dtos.append(PlanDTO(
                id=plan.plan_id,
                name=plan.name,
                description=plan.description,
                price=plan.price,
                duration_days=plan.duration_days,
                tier=plan.tier,
                features=features,
                is_active=plan.is_active,
                created_at=plan.created_at,
                updated_at=plan.updated_at,
            ))
        
        return PlanListResponseDTO(plans=plan_dtos, total=len(plan_dtos))


class PurchasePlanUseCase:
    """Use case for purchasing a subscription plan."""

    def __init__(
        self,
        plan_repository: PlanRepository,
        subscription_repository: SubscriptionRepository,
        user_repository: UserRepository,
    ):
        self.plan_repository = plan_repository
        self.subscription_repository = subscription_repository
        self.user_repository = user_repository

    def execute(self, request: PurchasePlanRequestDTO, user_id: int) -> PurchasePlanResponseDTO:
        """Execute the use case."""
        # Verify plan exists
        plan = self.plan_repository.find_by_id(request.plan_id)
        if not plan or not plan.is_active:
            raise ResourceNotFoundError(f"Plan {request.plan_id} not found or inactive")
        
        # Verify user exists
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ResourceNotFoundError(f"User {user_id} not found")
        
        # Create pending subscription
        now = datetime.utcnow()
        start_date = now
        end_date = now + timedelta(days=plan.duration_days)
        
        # Generate payment reference (in production, this would come from payment gateway)
        payment_reference = f"PAY-{user_id}-{plan.plan_id}-{int(now.timestamp())}"
        
        subscription = Subscription(
            subscription_id=0,  # Will be set by repository
            user_id=user_id,
            plan_id=plan.plan_id,
            status=SubscriptionStatus.PENDING,
            start_date=start_date,
            end_date=end_date,
            payment_reference=payment_reference,
        )
        
        saved_subscription = self.subscription_repository.create(subscription)
        
        return PurchasePlanResponseDTO(
            subscription_id=saved_subscription.subscription_id,
            payment_reference=payment_reference,
            status="pending",
            message="Subscription created. Please complete payment.",
        )


class VerifyPaymentUseCase:
    """Use case for verifying payment and activating subscription."""

    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
        user_repository: UserRepository,
        plan_repository: Optional[PlanRepository] = None,
        notification_service = None,
    ):
        self.subscription_repository = subscription_repository
        self.user_repository = user_repository
        self.plan_repository = plan_repository
        self.notification_service = notification_service

    def execute(self, request: VerifyPaymentRequestDTO) -> VerifyPaymentResponseDTO:
        """Execute the use case."""
        # Find subscription by payment reference
        subscription = self.subscription_repository.find_by_payment_reference(
            request.payment_reference
        )
        
        if not subscription:
            raise ResourceNotFoundError(f"Subscription with payment reference {request.payment_reference} not found")
        
        # In production, verify payment with payment gateway here
        # For now, we'll just activate the subscription
        
        subscription.status = SubscriptionStatus.ACTIVE
        updated_subscription = self.subscription_repository.update(subscription)
        
        # Update user tier based on plan (if plan_repository provided)
        if self.plan_repository:
            plan = self.plan_repository.find_by_id(subscription.plan_id)
            if plan:
                user = self.user_repository.find_by_id(subscription.user_id)
                if user:
                    user.tier = plan.tier
                    self.user_repository.update(user)
        
        # Create notification for user (if notification_service provided)
        if self.notification_service and self.plan_repository:
            plan = self.plan_repository.find_by_id(subscription.plan_id)
            if plan:
                self.notification_service.notify_subscription_activated(
                    user_id=subscription.user_id,
                    plan_name=plan.name,
                    subscription_id=updated_subscription.subscription_id,
                )
        
        return VerifyPaymentResponseDTO(
            success=True,
            subscription_id=updated_subscription.subscription_id,
            status="active",
            message="Payment verified and subscription activated",
        )


class GetUserSubscriptionUseCase:
    """Use case for getting user's current subscription."""

    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
        plan_repository: PlanRepository,
    ):
        self.subscription_repository = subscription_repository
        self.plan_repository = plan_repository

    def execute(self, user_id: int) -> SubscriptionDTO:
        """Execute the use case."""
        subscription = self.subscription_repository.find_active_by_user_id(user_id)
        
        if not subscription:
            raise ResourceNotFoundError(f"No active subscription found for user {user_id}")
        
        plan = self.plan_repository.find_by_id(subscription.plan_id)
        plan_name = plan.name if plan else "Unknown Plan"
        
        return SubscriptionDTO(
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
        )
