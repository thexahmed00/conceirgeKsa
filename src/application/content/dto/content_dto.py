"""Content DTOs - Banners and Cities."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class BannerDTO(BaseModel):
    """DTO for a banner."""
    id: int
    title: str
    image_url: str
    description: Optional[str] = None
    link_url: Optional[str] = None
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BannerListResponseDTO(BaseModel):
    """DTO for list of banners."""
    banners: List[BannerDTO]
    total: int


class CityDTO(BaseModel):
    """DTO for a city."""
    id: int
    name: str
    name_ar: Optional[str] = None
    country: str
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CityListResponseDTO(BaseModel):
    """DTO for list of cities."""
    cities: List[CityDTO]
    total: int
