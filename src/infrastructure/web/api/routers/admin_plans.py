"""Admin Plans API endpoints - plan management."""

import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.application.plan.dto.plan_dto import (
    PlanDTO,
    PlanListResponseDTO,
    SubscriptionDTO,
    CreatePlanRequestDTO,
    UpdatePlanRequestDTO,
)
from src.application.plan.use_cases.plan_use_cases import ListPlansUseCase
from src.application.plan.use_cases.admin_plan_use_cases import (
    CreatePlanUseCase,
    UpdatePlanUseCase,
    DeletePlanUseCase,
)
from src.application.plan.use_cases.admin_subscription_use_cases import (
    ListAllSubscriptionsUseCase,
)
from src.infrastructure.web.dependencies import (
    get_current_admin_user,
    get_plan_repository,
    get_subscription_repository,
)
from src.infrastructure.persistence.repositories.plan.plan_repository import PostgreSQLPlanRepository
from src.infrastructure.persistence.repositories.plan.subscription_repository import PostgreSQLSubscriptionRepository
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/admin/plans",
    tags=["admin-plans"],
)


@router.get("", response_model=PlanListResponseDTO, summary="Get all plans (admin)")
async def list_all_plans(
    admin_user_id: int = Depends(get_current_admin_user),
    plan_repo: PostgreSQLPlanRepository = Depends(get_plan_repository),
) -> PlanListResponseDTO:
    """
    List all plans including inactive ones (admin only).
    """
    plans = plan_repo.find_all(active_only=False)
    
    plan_dtos = []
    for plan in plans:
        features = None
        if plan.features:
            try:
                features = json.loads(plan.features)
            except (json.JSONDecodeError, TypeError):
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


@router.post("", response_model=PlanDTO, status_code=status.HTTP_201_CREATED, summary="Create a new plan (admin)")
async def create_plan(
    request: CreatePlanRequestDTO,
    admin_user_id: int = Depends(get_current_admin_user),
    plan_repo: PostgreSQLPlanRepository = Depends(get_plan_repository),
) -> PlanDTO:
    """
    Create a new subscription plan (admin only).
    """
    use_case = CreatePlanUseCase(plan_repo)
    return await use_case.execute(
        name=request.name,
        description=request.description,
        price=request.price,
        duration_days=request.duration_days,
        tier=request.tier,
        features=request.features,
        is_active=request.is_active,
    )


@router.put("/{plan_id}", response_model=PlanDTO, summary="Update a plan (admin)")
async def update_plan(
    plan_id: int,
    request: UpdatePlanRequestDTO,
    admin_user_id: int = Depends(get_current_admin_user),
    plan_repo: PostgreSQLPlanRepository = Depends(get_plan_repository),
) -> PlanDTO:
    """
    Update an existing subscription plan (admin only).
    """
    use_case = UpdatePlanUseCase(plan_repo)
    return await use_case.execute(
        plan_id=plan_id,
        name=request.name,
        description=request.description,
        price=request.price,
        duration_days=request.duration_days,
        tier=request.tier,
        features=request.features,
        is_active=request.is_active,
    )


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a plan (admin)")
async def delete_plan(
    plan_id: int,
    admin_user_id: int = Depends(get_current_admin_user),
    plan_repo: PostgreSQLPlanRepository = Depends(get_plan_repository),
):
    """
    Delete a subscription plan (admin only).
    """
    use_case = DeletePlanUseCase(plan_repo)
    success = await use_case.execute(plan_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan {plan_id} not found"
        )
    
    return None


@router.get("/subscriptions", response_model=List[SubscriptionDTO], summary="Get user subscriptions (admin)")
async def list_user_subscriptions(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    admin_user_id: int = Depends(get_current_admin_user),
    subscription_repo: PostgreSQLSubscriptionRepository = Depends(get_subscription_repository),
    plan_repo: PostgreSQLPlanRepository = Depends(get_plan_repository),
) -> List[SubscriptionDTO]:
    """
    List subscriptions, optionally filtered by user (admin only).
    """
    use_case = ListAllSubscriptionsUseCase(subscription_repo, plan_repo)
    return await use_case.execute(user_id=user_id)
