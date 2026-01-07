"""Banner domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Banner:
    """
    Banner entity represents a promotional banner displayed in the app.
    """
    banner_id: int
    title: str
    image_url: str
    description: Optional[str] = None
    link_url: Optional[str] = None  # Optional deep link or URL
    display_order: int = 0
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
