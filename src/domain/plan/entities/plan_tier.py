"""Plan tier enumeration."""

from enum import Enum


class PlanTier(str, Enum):
    """Plan tier enum representing different subscription levels."""
    
    LIFESTYLE = "Lifestyle"
    TRAVELLER = "Traveller"
    ELITE = "Elite"
    
    def __str__(self) -> str:
        """Return the tier name."""
        return self.value
    
    @classmethod
    def from_price(cls, price: float) -> "PlanTier":
        """Get tier from price point (for backward compatibility)."""
        price_mapping = {
            4999: cls.LIFESTYLE,
            24999: cls.TRAVELLER,
        }
        if price >= 24999:
            return cls.ELITE
        elif price >= 4999:
            return cls.TRAVELLER
        return cls.LIFESTYLE
