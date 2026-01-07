"""Plans API endpoints - subscription plans and purchases."""

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.plan.dto.plan_dto import (
    PlanListResponseDTO,
    SubscriptionDTO,
    PurchasePlanRequestDTO,
    PurchasePlanResponseDTO,
    VerifyPaymentRequestDTO,
    VerifyPaymentResponseDTO,
)
from src.application.plan.use_cases.plan_use_cases import (
    ListPlansUseCase,
    PurchasePlanUseCase,
    VerifyPaymentUseCase,
    GetUserSubscriptionUseCase,
)
from src.infrastructure.web.dependencies import (
    get_current_user,
    get_list_plans_use_case,
    get_purchase_plan_use_case,
    get_verify_payment_use_case,
    get_user_subscription_use_case,
)
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/plans",
    tags=["plans"],
)


@router.get("", response_model=PlanListResponseDTO, summary="Get all available plans")
def list_plans(
    use_case: ListPlansUseCase = Depends(get_list_plans_use_case),
) -> PlanListResponseDTO:
    """
    List all available subscription plans.
    
    Returns plans with details like price, duration, tier level, and features.
    """
    return use_case.execute()


@router.post("/purchase", response_model=PurchasePlanResponseDTO, summary="Purchase a subscription plan")
def purchase_plan(
    request: PurchasePlanRequestDTO,
    user_id: int = Depends(get_current_user),
    use_case: PurchasePlanUseCase = Depends(get_purchase_plan_use_case),
) -> PurchasePlanResponseDTO:
    """
    Purchase a subscription plan.
    
    Creates a pending subscription and returns payment reference for payment gateway integration.
    """
    return use_case.execute(request, user_id)


@router.post("/verify-payment", response_model=VerifyPaymentResponseDTO, summary="Verify payment and activate subscription")
def verify_payment(
    request: VerifyPaymentRequestDTO,
    user_id: int = Depends(get_current_user),
    use_case: VerifyPaymentUseCase = Depends(get_verify_payment_use_case),
) -> VerifyPaymentResponseDTO:
    """
    Verify payment and activate subscription.
    
    This endpoint should be called after successful payment to activate the subscription.
    """
    return use_case.execute(request)


@router.get("/my-subscription", response_model=SubscriptionDTO, summary="Get current user's active subscription")
def get_my_subscription(
    user_id: int = Depends(get_current_user),
    use_case: GetUserSubscriptionUseCase = Depends(get_user_subscription_use_case),
) -> SubscriptionDTO:
    """
    Get the current user's active subscription details.
    
    Returns subscription info including plan details, status, and days remaining.
    """
    return use_case.execute(user_id)
