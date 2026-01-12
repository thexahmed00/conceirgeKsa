"""Service DTOs - API input/output schemas."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# =============================================================================
# Restaurant Metadata DTOs (for structured input validation)
# =============================================================================

class OperatingHoursDTO(BaseModel):
    """Single operating hours entry for a restaurant."""
    name: str = Field(
        ...,
        description="Day/period label (e.g., 'Mon-Thu', 'Fri-Sun', 'Weekdays')"
    )
    time: str = Field(
        ...,
        description="Time range (e.g., '11:00 AM - 11:00 PM')"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mon-Thu",
                "time": "11:00 AM - 11:00 PM"
            }
        }


class DishDTO(BaseModel):
    """Single dish in a course."""
    name: str = Field(..., description="Dish name")
    image: Optional[str] = Field(None, description="Dish image URL")
    price: Optional[str] = Field(None, description="Dish price (e.g., '120 SAR')")
    description: Optional[str] = Field(None, description="Dish description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Grilled Salmon",
                "image": "https://images.unsplash.com/photo-salmon.jpg",
                "price": "120 SAR",
                "description": "Fresh Atlantic salmon with herbs"
            }
        }


class CourseDTO(BaseModel):
    """A course category containing multiple dishes."""
    name: str = Field(..., description="Course name (e.g., 'Main Course', 'Appetizers', 'Desserts')")
    dishes: List[DishDTO] = Field(default_factory=list, description="List of dishes in this course")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Main Course",
                "dishes": [
                    {"name": "Grilled Salmon", "image": "https://...", "price": "120 SAR"},
                    {"name": "Pasta Carbonara", "image": "https://...", "price": "85 SAR"}
                ]
            }
        }


class RestaurantMetadataDTO(BaseModel):
    """Structured metadata for restaurant vendors."""
    cuisine: Optional[str] = Field(None, description="Cuisine type (e.g., 'Italian - Mediterranean')")
    hours: List[OperatingHoursDTO] = Field(
        default_factory=list,
        description="Operating hours as array of day/time entries"
    )
    courses: List[CourseDTO] = Field(
        default_factory=list,
        description="Menu organized by courses, each containing dishes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "cuisine": "Italian - Mediterranean",
                "hours": [
                    {"name": "Mon-Thu", "time": "12:00 PM - 11:00 PM"},
                    {"name": "Fri-Sun", "time": "12:00 PM - 12:30 AM"}
                ],
                "courses": [
                    {
                        "name": "Appetizers",
                        "dishes": [
                            {"name": "Bruschetta", "image": "https://...", "price": "45 SAR"}
                        ]
                    },
                    {
                        "name": "Main Course",
                        "dishes": [
                            {"name": "Grilled Salmon", "image": "https://...", "price": "120 SAR"},
                            {"name": "Pasta Carbonara", "image": "https://...", "price": "85 SAR"}
                        ]
                    }
                ]
            }
        }


# =============================================================================
# Hotel Metadata DTOs (for structured input validation)
# =============================================================================

class AmenityDTO(BaseModel):
    """Single amenity for a hotel."""
    name: str = Field(..., description="Amenity name (e.g., 'Free WiFi', 'Swimming Pool')")
    icon: Optional[str] = Field(None, description="Icon name or URL (e.g., 'wifi', 'pool', or full URL)")
    subtitle: Optional[str] = Field(None, description="Additional detail about the amenity")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Free WiFi",
                "icon": "wifi",
                "subtitle": "Available in all rooms and lobby"
            }
        }


class NearbyAttractionDTO(BaseModel):
    """Nearby attraction/point of interest for a hotel."""
    name: str = Field(..., description="Attraction name")
    distance: Optional[str] = Field(None, description="Distance from hotel (e.g., '2.5 km', '10 min walk')")
    icon: Optional[str] = Field(None, description="Icon name or URL")
    category: Optional[str] = Field(None, description="Category (e.g., 'Shopping', 'Dining', 'Entertainment')")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Kingdom Centre Tower",
                "distance": "2.5 km",
                "icon": "landmark",
                "category": "Landmark"
            }
        }


class RoomTypeDTO(BaseModel):
    """Room type available at the hotel."""
    name: str = Field(..., description="Room type name (e.g., 'Deluxe Suite', 'Standard Room')")
    price: Optional[str] = Field(None, description="Price per night (e.g., '850 SAR/night')")
    image: Optional[str] = Field(None, description="Room image URL")
    description: Optional[str] = Field(None, description="Room description")
    capacity: Optional[str] = Field(None, description="Max occupancy (e.g., '2 Adults, 1 Child')")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Deluxe Suite",
                "price": "850 SAR/night",
                "image": "https://images.unsplash.com/photo-suite.jpg",
                "description": "Spacious suite with city view",
                "capacity": "2 Adults, 1 Child"
            }
        }


class HotelMetadataDTO(BaseModel):
    """Structured metadata for hotel vendors."""
    star_rating: Optional[int] = Field(None, ge=1, le=5, description="Hotel star rating (1-5)")
    check_in: Optional[str] = Field(None, description="Check-in time (e.g., '3:00 PM')")
    check_out: Optional[str] = Field(None, description="Check-out time (e.g., '12:00 PM')")
    amenities: List[AmenityDTO] = Field(
        default_factory=list,
        description="List of hotel amenities with icons and subtitles"
    )
    nearby_attractions: List[NearbyAttractionDTO] = Field(
        default_factory=list,
        description="Nearby points of interest"
    )
    room_types: List[RoomTypeDTO] = Field(
        default_factory=list,
        description="Available room types"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "star_rating": 5,
                "check_in": "3:00 PM",
                "check_out": "12:00 PM",
                "amenities": [
                    {"name": "Free WiFi", "icon": "wifi", "subtitle": "High-speed in all areas"},
                    {"name": "Swimming Pool", "icon": "pool", "subtitle": "Rooftop infinity pool"},
                    {"name": "Spa & Wellness", "icon": "spa", "subtitle": "Full-service spa"},
                    {"name": "Fitness Center", "icon": "fitness", "subtitle": "24/7 access"}
                ],
                "nearby_attractions": [
                    {"name": "Kingdom Centre Tower", "distance": "2.5 km", "icon": "landmark", "category": "Landmark"},
                    {"name": "Al Nakheel Mall", "distance": "1.2 km", "icon": "shopping", "category": "Shopping"},
                    {"name": "King Fahd Park", "distance": "3 km", "icon": "park", "category": "Recreation"}
                ],
                "room_types": [
                    {"name": "Deluxe Suite", "price": "850 SAR/night", "image": "https://...", "capacity": "2 Adults"}
                ]
            }
        }


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
    city: Optional[str] = None
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
    
    # Location
    city: Optional[str] = None
    
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
    
    # Location
    city: Optional[str] = Field(None, max_length=100, description="City where vendor operates (e.g., Riyadh, Jeddah)")
    
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
                "city": "Riyadh",
                "address": "1568 London Road, Rosalynnmouth 21327",
                "phone": "+123 456 789",
                "website": "www.CafeBonjour.com",
                "whatsapp": "+123 456 789",
                "rating": 4.2,
                "metadata": {
                    "cuisine": "Italian - Mediterranean",
                    "hours": [
                        {"name": "Mon-Thu", "time": "12:00 PM - 11:00 PM"},
                        {"name": "Fri-Sun", "time": "12:00 PM - 12:30 AM"}
                    ],
                    "courses": [
                        {
                            "name": "Appetizers",
                            "dishes": [
                                {"name": "Bruschetta", "image": "https://images.unsplash.com/photo-bruschetta.jpg", "price": "45 SAR"}
                            ]
                        },
                        {
                            "name": "Main Course",
                            "dishes": [
                                {"name": "Bistro Delights", "image": "https://images.unsplash.com/photo-bistro.jpg", "price": "120 SAR"},
                                {"name": "Grilled Salmon", "image": "https://images.unsplash.com/photo-salmon.jpg", "price": "150 SAR"}
                            ]
                        },
                        {
                            "name": "Elixirs",
                            "dishes": [
                                {"name": "Azure Cafe", "image": "https://images.unsplash.com/photo-coffee.jpg", "price": "35 SAR"}
                            ]
                        }
                    ]
                }
            },
            "example_hotel": {
                "category_slug": "hotel",
                "name": "The Ritz-Carlton Riyadh",
                "description": "Experience unparalleled luxury at The Ritz-Carlton Riyadh, featuring world-class amenities, stunning views, and exceptional service in the heart of the capital.",
                "city": "Riyadh",
                "address": "Al Hada Area, Mekkah Road",
                "phone": "+966 11 802 8020",
                "website": "www.ritzcarlton.com/riyadh",
                "whatsapp": "+966 11 802 8020",
                "rating": 4.9,
                "metadata": {
                    "star_rating": 5,
                    "check_in": "3:00 PM",
                    "check_out": "12:00 PM",
                    "amenities": [
                        {"name": "Free WiFi", "icon": "wifi", "subtitle": "High-speed in all areas"},
                        {"name": "Swimming Pool", "icon": "pool", "subtitle": "Rooftop infinity pool"},
                        {"name": "Spa & Wellness", "icon": "spa", "subtitle": "Full-service luxury spa"},
                        {"name": "Fitness Center", "icon": "fitness", "subtitle": "24/7 access"},
                        {"name": "Restaurant", "icon": "restaurant", "subtitle": "Fine dining options"},
                        {"name": "Room Service", "icon": "room_service", "subtitle": "24-hour service"}
                    ],
                    "nearby_attractions": [
                        {"name": "Kingdom Centre Tower", "distance": "2.5 km", "icon": "landmark", "category": "Landmark"},
                        {"name": "Al Nakheel Mall", "distance": "1.2 km", "icon": "shopping", "category": "Shopping"},
                        {"name": "King Fahd Park", "distance": "3 km", "icon": "park", "category": "Recreation"},
                        {"name": "National Museum", "distance": "5 km", "icon": "museum", "category": "Culture"}
                    ],
                    "room_types": [
                        {"name": "Deluxe Room", "price": "650 SAR/night", "image": "https://images.unsplash.com/photo-deluxe.jpg", "capacity": "2 Adults"},
                        {"name": "Executive Suite", "price": "1200 SAR/night", "image": "https://images.unsplash.com/photo-suite.jpg", "capacity": "2 Adults, 1 Child"},
                        {"name": "Royal Suite", "price": "3500 SAR/night", "image": "https://images.unsplash.com/photo-royal.jpg", "capacity": "4 Adults"}
                    ]
                }
            }
        }


class VendorUpdateDTO(BaseModel):
    """Input for updating a vendor."""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = Field(None, min_length=10)
    city: Optional[str] = Field(None, max_length=100)
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
                "city": "Riyadh",
                "rating": 4.5,
                "metadata": {
                    "cuisine": "Italian - Mediterranean",
                    "hours": [
                        {"name": "Mon-Thu", "time": "12:00 PM - 11:00 PM"},
                        {"name": "Fri-Sun", "time": "12:00 PM - 12:30 AM"}
                    ],
                    "courses": [
                        {
                            "name": "Main Course",
                            "dishes": [
                                {"name": "Bistro Delights", "image": "https://images.unsplash.com/photo-bistro.jpg", "price": "120 SAR"},
                                {"name": "New Dish", "image": "https://images.unsplash.com/photo-newdish.jpg", "price": "95 SAR"}
                            ]
                        },
                        {
                            "name": "Sweet Endings",
                            "dishes": [
                                {"name": "Tiramisu", "image": "https://images.unsplash.com/photo-tiramisu.jpg", "price": "55 SAR"}
                            ]
                        }
                    ]
                }
            },
            "example_hotel": {
                "name": "The Ritz-Carlton Riyadh Updated",
                "rating": 5.0,
                "metadata": {
                    "star_rating": 5,
                    "check_in": "2:00 PM",
                    "check_out": "1:00 PM",
                    "amenities": [
                        {"name": "Free WiFi", "icon": "wifi", "subtitle": "Ultra-fast fiber connection"},
                        {"name": "Private Beach", "icon": "beach", "subtitle": "Exclusive guest access"},
                        {"name": "Helipad", "icon": "helicopter", "subtitle": "VIP arrivals"}
                    ],
                    "nearby_attractions": [
                        {"name": "Boulevard Riyadh", "distance": "1 km", "icon": "entertainment", "category": "Entertainment"},
                        {"name": "Diriyah", "distance": "15 km", "icon": "historic", "category": "Heritage"}
                    ],
                    "room_types": [
                        {"name": "Presidential Suite", "price": "8000 SAR/night", "image": "https://...", "capacity": "6 Adults"}
                    ]
                }
            }
        }
