"""Service DTOs - API input/output schemas."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# =============================================================================
# Service Category DTOs
# =============================================================================

class ServiceCategoryResponseDTO(BaseModel):
    """Output for service category."""
    id: int
    slug: str
    name: str
    icon_url: Optional[str] = None
    display_order: int
    
    class Config:
        from_attributes = True


class ServiceCategoryListResponseDTO(BaseModel):
    """List of all service categories."""
    categories: List[ServiceCategoryResponseDTO]


# Admin input DTOs for categories
class ServiceCategoryCreateDTO(BaseModel):
    """Input for creating a service category."""
    slug: str = Field(..., min_length=2, description="Category slug (unique)")
    name: str = Field(..., min_length=2, description="Display name")
    display_order: int = Field(0, description="Display ordering integer")
    icon_url: Optional[str] = Field(None, description="Optional icon URL for the category")


class ServiceCategoryUpdateDTO(BaseModel):
    """Input for updating a service category."""
    name: Optional[str] = Field(None, min_length=2)
    display_order: Optional[int] = None
    icon_url: Optional[str] = None


# =============================================================================
# Vendor Image DTOs
# =============================================================================

class VendorImageDTO(BaseModel):
    """Output for vendor image metadata."""
    id: int
    image_type: str
    url: str  # Direct image URL (S3, Unsplash, etc.)
    thumbnail_url: Optional[str] = None
    caption: Optional[str] = None
    display_order: int
    
    class Config:
        from_attributes = True


class ImageCreateDTO(BaseModel):
    """Input for creating a vendor image."""
    image_type: str = Field(
        ...,
        description="Image type: 'hero' for carousel, 'gallery' for gallery"
    )
    image_url: str = Field(
        ...,
        description="Image URL (e.g., S3 URL or Unsplash URL)"
    )
    thumbnail_url: Optional[str] = Field(
        None,
        description="Optional thumbnail URL"
    )
    caption: Optional[str] = Field(
        None,
        max_length=255,
        description="Optional image caption"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_type": "hero",
                "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
                "caption": "Restaurant entrance"
            }
        }


class ImageReorderDTO(BaseModel):
    """Input for reordering images."""
    image_ids: List[int] = Field(
        ...,
        description="List of image IDs in desired order"
    )


# =============================================================================
# Vendor List DTOs
# =============================================================================

class VendorListItemDTO(BaseModel):
    """Output for vendor in list view (minimal data)."""
    id: int
    name: str
    category_slug: Optional[str] = None
    category_name: Optional[str] = None
    thumbnail_url: Optional[str] = None  # First hero image thumbnail
    rating: float
    short_description: str  # Truncated description
    address: Optional[str] = None
    
    class Config:
        from_attributes = True


class VendorListResponseDTO(BaseModel):
    """Paginated list of vendors."""
    vendors: List[VendorListItemDTO]
    total: int
    skip: int
    limit: int


# =============================================================================
# Vendor Detail DTOs
# =============================================================================

class VendorDetailDTO(BaseModel):
    """Output for full vendor details."""
    id: int
    category_id: int
    category_slug: Optional[str] = None
    category_name: Optional[str] = None
    
    # Basic info
    name: str
    description: str
    
    # Contact
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    whatsapp: Optional[str] = None
    
    # Rating
    rating: float
    
    # Images
    hero_images: List[VendorImageDTO] = []
    gallery_images: List[VendorImageDTO] = []
    
    # Type-specific metadata (dishes, rooms, aircraft, etc.)
    metadata: Dict[str, Any] = {}
    
    # Status
    is_active: bool
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# =============================================================================
# Admin Vendor DTOs
# =============================================================================

class VendorCreateDTO(BaseModel):
    """Input for creating a new vendor."""
    category_slug: str = Field(
        ...,
        description="Category slug (restaurant, hotel, private_jet, etc.)"
    )
    name: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Vendor name"
    )
    description: str = Field(
        ...,
        min_length=10,
        description="Vendor description"
    )
    
    # Contact (optional)
    address: Optional[str] = Field(None, max_length=500)
    phone: Optional[str] = Field(None, max_length=50)
    website: Optional[str] = Field(None, max_length=255)
    whatsapp: Optional[str] = Field(None, max_length=50)
    
    # Rating
    rating: float = Field(0.0, ge=0, le=5)
    
    # Type-specific metadata
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Type-specific data (hours, dishes, rooms, etc.)"
    )
    
    # Activation status
    is_active: bool = Field(True, description="Whether vendor is visible to users")
    
    class Config:
        json_schema_extra = {
            "example": {
                "category_slug": "restaurant",
                "name": "Cafe Bonjour",
                "description": "Experience authentic Italian flavors with a modern touch. Cafe Bonjour is known for its handmade pasta, wood-fired pizza, and romantic candle-lit ambiance.",
                "address": "1568 London Road, Rosalynnmouth 21327",
                "phone": "+123 456 789",
                "website": "www.CafeBonjour.com",
                "whatsapp": "+123 456 789",
                "rating": 4.2,
                "metadata": {
                    "cuisine": "Italian – Mediterranean",
                    "hours": {
                        "mon_thu": "12:00 PM – 11:00 PM",
                        "fri_sun": "12:00 PM – 12:30 AM"
                    },
                    "dishes": [
                        {"name": "Bistro Delights", "category": "Main Course"},
                        {"name": "Azure Cafe", "category": "Elixirs"}
                    ]
                }
            }
        }


class VendorUpdateDTO(BaseModel):
    """Input for updating a vendor."""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = Field(None, min_length=10)
    address: Optional[str] = Field(None, max_length=500)
    phone: Optional[str] = Field(None, max_length=50)
    website: Optional[str] = Field(None, max_length=255)
    whatsapp: Optional[str] = Field(None, max_length=50)
    rating: Optional[float] = Field(None, ge=0, le=5)
    metadata: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Cafe Bonjour Updated",
                "rating": 4.5,
                "metadata": {
                    "cuisine": "Italian – Mediterranean",
                    "hours": {
                        "mon_thu": "12:00 PM – 11:00 PM",
                        "fri_sun": "12:00 PM – 12:30 AM"
                    },
                    "dishes": [
                        {"name": "Bistro Delights", "category": "Main Course", "image_base64": "..."},
                        {"name": "New Dish", "category": "Sweet Endings"}
                    ]
                }
            }
        }
