"""Plan DTOs."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class PlanDTO(BaseModel):
    """DTO for a subscription plan."""
    id: int
    name: str
    description: str
    price: float
    duration_days: int
    tier: int
    features: Optional[List[str]] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PlanListResponseDTO(BaseModel):
    """DTO for list of plans."""
    plans: List[PlanDTO]
    total: int


class SubscriptionDTO(BaseModel):
    """DTO for a user subscription."""
    id: int
    user_id: int
    plan_id: int
    plan_name: str
    status: str
    start_date: datetime
    end_date: datetime
    days_remaining: int = 0
    payment_reference: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PurchasePlanRequestDTO(BaseModel):
    """DTO for purchasing a plan."""
    plan_id: int = Field(..., description="ID of the plan to purchase")
    payment_method: str = Field(..., description="Payment method (e.g., 'credit_card', 'mada', 'apple_pay')")


class PurchasePlanResponseDTO(BaseModel):
    """DTO for plan purchase response."""
    subscription_id: int
    payment_reference: str
    status: str
    message: str


class VerifyPaymentRequestDTO(BaseModel):
    """DTO for payment verification."""
    payment_reference: str = Field(..., description="Payment gateway reference ID")
    transaction_id: Optional[str] = Field(None, description="Optional transaction ID from payment gateway")


class VerifyPaymentResponseDTO(BaseModel):
    """DTO for payment verification response."""
    success: bool
    subscription_id: int
    status: str
    message: str


class CreatePlanRequestDTO(BaseModel):
    """DTO for creating a plan (admin)."""
    name: str = Field(..., description="Plan name")
    description: str = Field(..., description="Plan description")
    price: float = Field(..., ge=0, description="Plan price")
    duration_days: int = Field(..., gt=0, description="Duration in days")
    tier: int = Field(..., ge=0, description="Tier level")
    features: Optional[List[str]] = Field(default=None, description="List of features")
    is_active: bool = Field(default=True, description="Whether plan is active")


class UpdatePlanRequestDTO(BaseModel):
    """DTO for updating a plan (admin)."""
    name: Optional[str] = Field(None, description="Plan name")
    description: Optional[str] = Field(None, description="Plan description")
    price: Optional[float] = Field(None, ge=0, description="Plan price")
    duration_days: Optional[int] = Field(None, gt=0, description="Duration in days")
    tier: Optional[int] = Field(None, ge=0, description="Tier level")
    features: Optional[List[str]] = Field(None, description="List of features")
    is_active: Optional[bool] = Field(None, description="Whether plan is active")
