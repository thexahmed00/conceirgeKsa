"""City domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class City:
    """
    City entity represents a city/location where services are available.
    """
    city_id: int
    name: str
    name_ar: Optional[str] = None  # Arabic name
    country: str = "Saudi Arabia"
    display_order: int = 0
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
