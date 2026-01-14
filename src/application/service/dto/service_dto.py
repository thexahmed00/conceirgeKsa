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
# Private Jet Metadata DTOs
# =============================================================================

class JetTypeDTO(BaseModel):
    """Aircraft type available for charter."""
    name: str = Field(..., description="Aircraft model name (e.g., 'Cessna Citation X', 'Gulfstream G650')")
    image: Optional[str] = Field(None, description="Aircraft image URL")
    capacity: Optional[str] = Field(None, description="Passenger capacity (e.g., '8-12 passengers')")
    range: Optional[str] = Field(None, description="Flight range (e.g., '6,000 nm')")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Gulfstream G650",
                "image": "https://images.unsplash.com/photo-jet.jpg",
                "capacity": "8-12 passengers",
                "range": "7,000 nm"
            }
        }


class PopularRouteDTO(BaseModel):
    """Popular flight route."""
    origin: str = Field(..., description="Origin city")
    destination: str = Field(..., description="Destination city")
    
    class Config:
        json_schema_extra = {
            "example": {
                "origin": "Riyadh",
                "destination": "London"
            }
        }


class PrivateJetMetadataDTO(BaseModel):
    """Structured metadata for private jet vendors."""
    hours: List[OperatingHoursDTO] = Field(
        default_factory=list,
        description="Operating hours / support availability"
    )
    languages: List[str] = Field(
        default_factory=list,
        description="Languages supported (e.g., ['English', 'Arabic', 'French'])"
    )
    service_area: List[str] = Field(
        default_factory=list,
        description="Service coverage (e.g., ['Domestic', 'International routes'])"
    )
    jet_types: List[JetTypeDTO] = Field(
        default_factory=list,
        description="Available aircraft types"
    )
    popular_routes: List[PopularRouteDTO] = Field(
        default_factory=list,
        description="Popular flight routes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "hours": [
                    {"name": "Open Hours", "time": "24/7 Concierge Support"}
                ],
                "languages": ["English", "Arabic", "French"],
                "service_area": ["Domestic", "International routes"],
                "jet_types": [
                    {"name": "Cessna Citation XLS+", "image": "https://...", "capacity": "8 passengers", "range": "2,100 nm"},
                    {"name": "Gulfstream G650", "image": "https://...", "capacity": "12 passengers", "range": "7,000 nm"},
                    {"name": "Bombardier Global 500", "image": "https://...", "capacity": "10 passengers", "range": "5,700 nm"}
                ],
                "popular_routes": [
                    {"origin": "Dubai", "destination": "Paris"},
                    {"origin": "Riyadh", "destination": "London"},
                    {"origin": "Los Angeles", "destination": "New York"},
                    {"origin": "Rome", "destination": "Mykonos"}
                ]
            }
        }


# =============================================================================
# Flight (Commercial) Metadata DTOs
# =============================================================================

class SeatTypeDTO(BaseModel):
    """Seat class available on flight."""
    name: str = Field(..., description="Seat class name (e.g., 'Economy', 'Business Class', 'First Class')")
    image: Optional[str] = Field(None, description="Seat class image URL")
    description: Optional[str] = Field(None, description="Description of amenities")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Business Class",
                "image": "https://images.unsplash.com/photo-business-seat.jpg",
                "description": "Lie-flat seats with premium dining"
            }
        }


class FlightMetadataDTO(BaseModel):
    """Structured metadata for flight/airline vendors."""
    hours: List[OperatingHoursDTO] = Field(
        default_factory=list,
        description="Operating hours / support availability"
    )
    languages: List[str] = Field(
        default_factory=list,
        description="Languages supported"
    )
    service_area: List[str] = Field(
        default_factory=list,
        description="Service coverage (e.g., ['Domestic', 'International routes'])"
    )
    seat_types: List[SeatTypeDTO] = Field(
        default_factory=list,
        description="Available seat classes"
    )
    popular_routes: List[PopularRouteDTO] = Field(
        default_factory=list,
        description="Popular flight routes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "hours": [
                    {"name": "Open Hours", "time": "24/7 Concierge Support"}
                ],
                "languages": ["English", "Arabic", "French"],
                "service_area": ["Domestic", "International routes"],
                "seat_types": [
                    {"name": "Economy", "image": "https://...", "description": "Standard seating with entertainment"},
                    {"name": "Business Class", "image": "https://...", "description": "Lie-flat seats with premium dining"},
                    {"name": "First Class", "image": "https://...", "description": "Private suites with exclusive amenities"}
                ],
                "popular_routes": [
                    {"origin": "Dubai", "destination": "Paris"},
                    {"origin": "Riyadh", "destination": "London"},
                    {"origin": "Los Angeles", "destination": "New York"},
                    {"origin": "Rome", "destination": "Mykonos"}
                ]
            }
        }


# =============================================================================
# Car Rental & Car with Driver Metadata DTOs
# =============================================================================

class CarBasicDTO(BaseModel):
    """Basic car specifications."""
    doors: Optional[str] = Field(None, description="Number of doors (e.g., '2 Doors', '4 Doors')")
    seats: Optional[str] = Field(None, description="Number of seats (e.g., '4 Seats', '7 Seats')")
    fuel_type: Optional[str] = Field(None, description="Fuel type (e.g., 'Gas', 'Electric', 'Hybrid')")
    transmission: Optional[str] = Field(None, description="Transmission type (e.g., 'Automatic', 'Manual')")
    
    class Config:
        json_schema_extra = {
            "example": {
                "doors": "2 Doors",
                "seats": "4 Seats",
                "fuel_type": "Gas",
                "transmission": "Automatic"
            }
        }


class ChauffeurDTO(BaseModel):
    """Chauffeur information for car with driver service."""
    name: str = Field(..., description="Chauffeur name")
    contact: Optional[str] = Field(None, description="Contact method (e.g., 'Message Khaled')")
    image: Optional[str] = Field(None, description="Chauffeur photo URL")
    languages: List[str] = Field(default_factory=list, description="Languages spoken")
    experience: Optional[str] = Field(None, description="Years of experience")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Khaled Hunter",
                "contact": "Message Khaled",
                "image": "https://images.unsplash.com/photo-chauffeur.jpg",
                "languages": ["Arabic", "English"],
                "experience": "10+ years"
            }
        }


class CarMetadataDTO(BaseModel):
    """Structured metadata for car rental vendors."""
    car_basic: Optional[CarBasicDTO] = Field(None, description="Basic car specifications")
    
    class Config:
        json_schema_extra = {
            "example": {
                "car_basic": {
                    "doors": "2 Doors",
                    "seats": "4 Seats",
                    "fuel_type": "Gas",
                    "transmission": "Automatic"
                }
            }
        }


class CarWithDriverMetadataDTO(BaseModel):
    """Structured metadata for car with driver vendors."""
    car_basic: Optional[CarBasicDTO] = Field(None, description="Basic car specifications")
    chauffeur: Optional[ChauffeurDTO] = Field(None, description="Chauffeur information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "car_basic": {
                    "doors": "2 Doors",
                    "seats": "4 Seats",
                    "fuel_type": "Gas",
                    "transmission": "Automatic"
                },
                "chauffeur": {
                    "name": "Khaled Hunter",
                    "contact": "Message Khaled",
                    "image": "https://...",
                    "languages": ["Arabic", "English"],
                    "experience": "10+ years"
                }
            }
        }


# =============================================================================
# Boat/Yacht Metadata DTOs
# =============================================================================

class BoatMetadataDTO(BaseModel):
    """Structured metadata for boat/yacht vendors."""
    crew: Optional[str] = Field(None, description="Crew info (e.g., 'Dedicated Captain & Hostess/Deckhand')")
    guests: Optional[str] = Field(None, description="Guest capacity (e.g., 'Up to 10 for cruising, 6 for overnight charters')")
    cabins: Optional[str] = Field(None, description="Cabin info (e.g., '3 En-Suite (Master, VIP, Twin)')")
    amenities: List[AmenityDTO] = Field(
        default_factory=list,
        description="Boat amenities and dedicated services"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "crew": "Dedicated Captain & Hostess/Deckhand",
                "guests": "Up to 10 for cruising, 6 for overnight charters",
                "cabins": "3 En-Suite (Master, VIP, Twin)",
                "amenities": [
                    {"name": "Dedicated workspace", "icon": "workspace"},
                    {"name": "Hot water", "icon": "hot_water"},
                    {"name": "Kitchen", "icon": "kitchen"},
                    {"name": "TV", "icon": "tv"},
                    {"name": "Air conditioning", "icon": "ac"},
                    {"name": "Microwave", "icon": "microwave"},
                    {"name": "WiFi", "icon": "wifi"},
                    {"name": "Refrigerator", "icon": "refrigerator"}
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
    
    # Images (optional - can add images during creation)
    hero_images: Optional[List[ImageCreateDTO]] = Field(
        default_factory=list,
        description="Hero images for carousel"
    )
    gallery_images: Optional[List[ImageCreateDTO]] = Field(
        default_factory=list,
        description="Gallery images"
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
                },
                "hero_images": [
                    {"image_type": "hero", "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1200", "thumbnail_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400", "caption": "Restaurant exterior"},
                    {"image_type": "hero", "image_url": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=1200", "thumbnail_url": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=400", "caption": "Elegant dining area"}
                ],
                "gallery_images": [
                    {"image_type": "gallery", "image_url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1200", "caption": "Signature dishes"},
                    {"image_type": "gallery", "image_url": "https://images.unsplash.com/photo-1555992336-fb0af0ff2bfc?w=1200", "caption": "Wood-fired pizza oven"}
                ],
                "is_active": true
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
                },
                "hero_images": [
                    {"image_type": "hero", "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200", "caption": "Hotel exterior"},
                    {"image_type": "hero", "image_url": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=1200", "caption": "Luxury lobby"}
                ],
                "gallery_images": [
                    {"image_type": "gallery", "image_url": "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=1200", "caption": "Deluxe room interior"},
                    {"image_type": "gallery", "image_url": "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=1200", "caption": "Rooftop infinity pool"}
                ],
                "is_active": true
            },
            "example_private_jet": {
                "category_slug": "private_jet",
                "name": "SkyLux Private Jets",
                "description": "SkyLux Private Jets offers luxury air travel for business executives, celebrities, and elite travelers. Choose from a premium fleet of private aircraft, with full concierge support—from personalized meals to airport transfers and in-flight entertainment.",
                "city": "Riyadh",
                "address": "VIP Terminal, City International Airport",
                "phone": "+123 999 000",
                "website": "www.SkyLux.com",
                "whatsapp": "+123 999 000",
                "rating": 5.0,
                "metadata": {
                    "hours": [
                        {"name": "Open Hours", "time": "24/7 Concierge Support"}
                    ],
                    "languages": ["English", "Arabic", "French"],
                    "service_area": ["Domestic", "International routes"],
                    "jet_types": [
                        {"name": "Cessna Citation XLS+", "image": "https://images.unsplash.com/photo-cessna.jpg", "capacity": "8 passengers", "range": "2,100 nm"},
                        {"name": "Gulfstream G650", "image": "https://images.unsplash.com/photo-gulfstream.jpg", "capacity": "12 passengers", "range": "7,000 nm"},
                        {"name": "Bombardier Global 500", "image": "https://images.unsplash.com/photo-bombardier.jpg", "capacity": "10 passengers", "range": "5,700 nm"}
                    ],
                    "popular_routes": [
                        {"origin": "Dubai", "destination": "Paris"},
                        {"origin": "Riyadh", "destination": "London"},
                        {"origin": "Los Angeles", "destination": "New York"},
                        {"origin": "Rome", "destination": "Mykonos"}
                    ]
                },
                "hero_images": [
                    {"image_type": "hero", "image_url": "https://images.unsplash.com/photo-1540962351504-03099e0a754b?w=1200", "caption": "Private jet exterior"},
                    {"image_type": "hero", "image_url": "https://images.unsplash.com/photo-1474302770737-173ee21bab63?w=1200", "caption": "Luxury cabin interior"}
                ],
                "gallery_images": [
                    {"image_type": "gallery", "image_url": "https://images.unsplash.com/photo-jet-interior.jpg?w=1200", "caption": "Premium seating"},
                    {"image_type": "gallery", "image_url": "https://images.unsplash.com/photo-jet-dining.jpg?w=1200", "caption": "In-flight dining"}
                ],
                "is_active": true
            },
            "example_flight": {
                "category_slug": "flight",
                "name": "Saudi Flight Airways",
                "description": "Saudi Flight Airways offers luxury air travel for business executives, celebrities, and elite travelers. Choose from a premium fleet of private aircraft, with full concierge support—from personalized meals to airport transfers and in-flight entertainment.",
                "city": "Riyadh",
                "address": "VIP Terminal, City International Airport",
                "phone": "+123 999 000",
                "website": "www.SkyLux.com",
                "whatsapp": "+123 999 000",
                "rating": 5.0,
                "metadata": {
                    "hours": [
                        {"name": "Open Hours", "time": "24/7 Concierge Support"}
                    ],
                    "languages": ["English", "Arabic", "French"],
                    "service_area": ["Domestic", "International routes"],
                    "seat_types": [
                        {"name": "Economy", "image": "https://images.unsplash.com/photo-economy.jpg", "description": "Standard seating with entertainment"},
                        {"name": "Business Class", "image": "https://images.unsplash.com/photo-business.jpg", "description": "Lie-flat seats with premium dining"},
                        {"name": "First Class", "image": "https://images.unsplash.com/photo-firstclass.jpg", "description": "Private suites with exclusive amenities"}
                    ],
                    "popular_routes": [
                        {"origin": "Dubai", "destination": "Paris"},
                        {"origin": "Riyadh", "destination": "London"},
                        {"origin": "Los Angeles", "destination": "New York"},
                        {"origin": "Rome", "destination": "Mykonos"}
                    ]
                },
                "hero_images": [
                    {"image_type": "hero", "image_url": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1200", "caption": "Aircraft exterior"},
                    {"image_type": "hero", "image_url": "https://images.unsplash.com/photo-1540339832862-474599807836?w=1200", "caption": "First class cabin"}
                ],
                "gallery_images": [
                    {"image_type": "gallery", "image_url": "https://images.unsplash.com/photo-flight-seat.jpg?w=1200", "caption": "Business class seat"},
                    {"image_type": "gallery", "image_url": "https://images.unsplash.com/photo-flight-meal.jpg?w=1200", "caption": "Premium dining"}
                ],
                "is_active": true
            },
            "example_car_rental": {
                "category_slug": "car_rental",
                "name": "2024 Rolls-Royce Ghost",
                "description": "The Rolls-Royce Ghost is not merely a car; it is a sanctuary. Engineered around a philosophy of 'post-opulence', it offers a profoundly quiet and effortless driving experience. For the discerning client who values understated power and peerless comfort over ostentation, the Ghost is the ultimate choice for executive travel, a special anniversary, or simply indulging in the finest automotive experience in the world.",
                "city": "Riyadh",
                "address": "Al Faisaliyah District, Riyadh",
                "phone": "+966 11 123 4567",
                "website": "www.luxurycars.sa",
                "whatsapp": "+966 11 123 4567",
                "rating": 5.0,
                "metadata": {
                    "car_basic": {
                        "doors": "2 Doors",
                        "seats": "4 Seats",
                        "fuel_type": "Gas",
                        "transmission": "Automatic"
                    }
                },
                "hero_images": [
                    {"image_type": "hero", "image_url": "https://images.unsplash.com/photo-rolls-royce.jpg?w=1200", "caption": "Rolls-Royce Ghost exterior"},
                    {"image_type": "hero", "image_url": "https://images.unsplash.com/photo-rr-interior.jpg?w=1200", "caption": "Luxury interior"}
                ],
                "gallery_images": [
                    {"image_type": "gallery", "image_url": "https://images.unsplash.com/photo-rr-dashboard.jpg?w=1200", "caption": "Starlight headliner"},
                    {"image_type": "gallery", "image_url": "https://images.unsplash.com/photo-rr-seats.jpg?w=1200", "caption": "Premium leather seats"}
                ],
                "is_active": true
            },
            "example_car_with_driver": {
                "category_slug": "car_driver",
                "name": "2024 Rolls-Royce Ghost with Chauffeur",
                "description": "The Rolls-Royce Ghost is not merely a car; it is a sanctuary. Engineered around a philosophy of 'post-opulence', it offers a profoundly quiet and effortless driving experience. For the discerning client who values understated power and peerless comfort over ostentation, the Ghost is the ultimate choice for executive travel, a special anniversary, or simply indulging in the finest automotive experience in the world.",
                "city": "Riyadh",
                "address": "Al Faisaliyah District, Riyadh",
                "phone": "+966 11 123 4567",
                "website": "www.luxurycars.sa",
                "whatsapp": "+966 11 123 4567",
                "rating": 5.0,
                "metadata": {
                    "car_basic": {
                        "doors": "2 Doors",
                        "seats": "4 Seats",
                        "fuel_type": "Gas",
                        "transmission": "Automatic"
                    },
                    "chauffeur": {
                        "name": "Khaled Hunter",
                        "contact": "Message Khaled",
                        "image": "https://images.unsplash.com/photo-chauffeur.jpg",
                        "languages": ["Arabic", "English"],
                        "experience": "10+ years"
                    }
                },
                "hero_images": [
                    {"image_type": "hero", "image_url": "https://images.unsplash.com/photo-rolls-royce.jpg?w=1200", "caption": "Rolls-Royce Ghost exterior"},
                    {"image_type": "hero", "image_url": "https://images.unsplash.com/photo-rr-interior.jpg?w=1200", "caption": "Luxury interior"}
                ],
                "gallery_images": [
                    {"image_type": "gallery", "image_url": "https://images.unsplash.com/photo-rr-dashboard.jpg?w=1200", "caption": "Starlight headliner"},
                    {"image_type": "gallery", "image_url": "https://images.unsplash.com/photo-chauffeur-service.jpg?w=1200", "caption": "Professional chauffeur service"}
                ],
                "is_active": true
            },
            "example_boat": {
                "category_slug": "boat",
                "name": "Serenity - 62ft Sunseeker Predator",
                "description": "'Serenity' is not just a yacht; it is a statement. This 62-foot Sunseeker Predator masterfully blends breathtaking performance with uncompromising luxury. Designed for the discerning guest who demands both exhilaration and relaxation, its sleek lines and powerful presence are matched only by its exceptionally spacious and elegant interior. Ideal for intimate celebrations, corporate entertaining, or a sublime day exploring the coastline in absolute style.",
                "city": "Jeddah",
                "address": "Marina Bay, Jeddah",
                "phone": "+966 12 345 6789",
                "website": "www.luxuryyachts.sa",
                "whatsapp": "+966 12 345 6789",
                "rating": 5.0,
                "metadata": {
                    "crew": "Dedicated Captain & Hostess/Deckhand",
                    "guests": "Up to 10 for cruising, 6 for overnight charters",
                    "cabins": "3 En-Suite (Master, VIP, Twin)",
                    "amenities": [
                        {"name": "Dedicated workspace", "icon": "workspace"},
                        {"name": "Hot water", "icon": "hot_water"},
                        {"name": "Kitchen", "icon": "kitchen"},
                        {"name": "TV", "icon": "tv"},
                        {"name": "Air conditioning", "icon": "ac"},
                        {"name": "Microwave", "icon": "microwave"},
                        {"name": "WiFi", "icon": "wifi"},
                        {"name": "Refrigerator", "icon": "refrigerator"}
                    ]
                },
                "hero_images": [
                    {"image_type": "hero", "image_url": "https://images.unsplash.com/photo-1567899378494-47b22a2ae96a?w=1200", "caption": "Yacht at sea"},
                    {"image_type": "hero", "image_url": "https://images.unsplash.com/photo-1569263979104-865ab7cd8d13?w=1200", "caption": "Deck view"}
                ],
                "gallery_images": [
                    {"image_type": "gallery", "image_url": "https://images.unsplash.com/photo-yacht-interior.jpg?w=1200", "caption": "Master cabin"},
                    {"image_type": "gallery", "image_url": "https://images.unsplash.com/photo-yacht-dining.jpg?w=1200", "caption": "Dining area"}
                ],
                "is_active": true
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
    hero_images: Optional[List[ImageCreateDTO]] = Field(
        None,
        description="Replace all hero images (if provided)"
    )
    gallery_images: Optional[List[ImageCreateDTO]] = Field(
        None,
        description="Replace all gallery images (if provided)"
    )
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
