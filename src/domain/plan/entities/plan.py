"""Plan domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Plan:
    """
    Plan entity represents a subscription plan tier.
    """
    plan_id: int
    name: str
    description: str
    price: float
    duration_days: int  # e.g., 30 for monthly, 365 for yearly
    tier: int  # Tier level (e.g., 5000, 10000, 15000)
    features: Optional[str] = None  # JSON string of features
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate plan data."""
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.duration_days <= 0:
            raise ValueError("Duration must be positive")
        if self.tier < 0:
            raise ValueError("Tier cannot be negative")
