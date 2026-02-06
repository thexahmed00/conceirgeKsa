"""Admin plan use cases."""

import json
from src.domain.plan.entities.plan import Plan
from src.domain.plan.entities.plan_tier import PlanTier
from src.domain.plan.repository.plan_repository import PlanRepository
from src.domain.shared.exceptions import ResourceNotFoundError
from src.application.plan.dto.plan_dto import PlanDTO


class CreatePlanUseCase:
    """Use case for creating a new plan (admin only)."""

    def __init__(self, plan_repository: PlanRepository):
        self.plan_repository = plan_repository

    async def execute(
        self,
        name: str,
        description: str,
        price: float,
        duration_days: int,
        tier: PlanTier,
        features: list = None,
        is_active: bool = True,
    ) -> PlanDTO:
        """Execute the use case."""
        # Convert features list to JSON string
        features_json = json.dumps(features) if features else None
        
        # Ensure tier is PlanTier enum
        if isinstance(tier, str):
            tier = PlanTier(tier)
        
        plan = Plan(
            plan_id=0,  # Will be set by repository
            name=name,
            description=description,
            price=price,
            duration_days=duration_days,
            tier=tier,
            features=features_json,
            is_active=is_active,
        )
        
        saved_plan = self.plan_repository.create(plan)
        
        # Parse features back to list for response
        features_list = json.loads(saved_plan.features) if saved_plan.features else []
        
        return PlanDTO(
            id=saved_plan.plan_id,
            name=saved_plan.name,
            description=saved_plan.description,
            price=saved_plan.price,
            duration_days=saved_plan.duration_days,
            tier=saved_plan.tier,
            features=features_list,
            is_active=saved_plan.is_active,
            created_at=saved_plan.created_at,
            updated_at=saved_plan.updated_at,
        )


class UpdatePlanUseCase:
    """Use case for updating a plan (admin only)."""

    def __init__(self, plan_repository: PlanRepository):
        self.plan_repository = plan_repository

    async def execute(
        self,
        plan_id: int,
        name: str = None,
        description: str = None,
        price: float = None,
        duration_days: int = None,
        tier: PlanTier = None,
        features: list = None,
        is_active: bool = None,
    ) -> PlanDTO:
        """Execute the use case."""
        plan = self.plan_repository.find_by_id(plan_id)
        if not plan:
            raise ResourceNotFoundError(f"Plan {plan_id} not found")
        
        # Update fields if provided
        if name is not None:
            plan.name = name
        if description is not None:
            plan.description = description
        if price is not None:
            plan.price = price
        if duration_days is not None:
            plan.duration_days = duration_days
        if tier is not None:
            # Ensure tier is PlanTier enum
            if isinstance(tier, str):
                tier = PlanTier(tier)
            plan.tier = tier
        if features is not None:
            plan.features = json.dumps(features)
        if is_active is not None:
            plan.is_active = is_active
        
        updated_plan = self.plan_repository.update(plan)
        
        # Parse features back to list for response
        features_list = json.loads(updated_plan.features) if updated_plan.features else []
        
        return PlanDTO(
            id=updated_plan.plan_id,
            name=updated_plan.name,
            description=updated_plan.description,
            price=updated_plan.price,
            duration_days=updated_plan.duration_days,
            tier=updated_plan.tier,
            features=features_list,
            is_active=updated_plan.is_active,
            created_at=updated_plan.created_at,
            updated_at=updated_plan.updated_at,
        )


class DeletePlanUseCase:
    """Use case for deleting a plan (admin only)."""

    def __init__(self, plan_repository: PlanRepository):
        self.plan_repository = plan_repository

    async def execute(self, plan_id: int) -> bool:
        """Execute the use case."""
        return self.plan_repository.delete(plan_id)
