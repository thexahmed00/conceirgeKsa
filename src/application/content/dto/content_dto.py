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


class BannerCreateDTO(BaseModel):
    """Admin DTO for creating a banner."""
    title: str = Field(..., min_length=1, max_length=255, description="Banner title/text on image")
    image_url: str = Field(..., description="Banner image URL (S3, Unsplash, etc.)")
    description: Optional[str] = Field(None, max_length=500, description="Optional banner description")
    link_url: Optional[str] = Field(None, max_length=500, description="Optional deep link or URL on click")
    display_order: int = Field(0, ge=0, description="Display order for sorting")
    is_active: bool = Field(True, description="Whether banner is visible to users")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Summer Sale 50% Off",
                "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
                "description": "Check out our summer collection with amazing discounts",
                "link_url": "app://promo/summer-2025",
                "display_order": 1,
                "is_active": True
            }
        }


class BannerUpdateDTO(BaseModel):
    """Admin DTO for updating a banner."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    image_url: Optional[str] = Field(None, description="Banner image URL")
    description: Optional[str] = Field(None, max_length=500)
    link_url: Optional[str] = Field(None, max_length=500)
    display_order: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Summer Sale 60% Off",
                "display_order": 2,
                "is_active": True
            }
        }


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
