"""ServiceVendor domain entity."""

from datetime import datetime
from typing import Optional, Dict, Any, List
from src.domain.shared.exceptions import DomainException


class InvalidVendorError(DomainException):
    """Raised when vendor data is invalid."""
    pass


class ServiceVendor:
    """ServiceVendor aggregate - represents a service provider (restaurant, hotel, etc.)."""
    
    def __init__(
        self,
        vendor_id: Optional[int],
        category_id: int,
        name: str,
        description: str,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        website: Optional[str] = None,
        whatsapp: Optional[str] = None,
        city: Optional[str] = None,
        rating: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        # Transient fields (not persisted on vendor, loaded from relationships)
        category_slug: Optional[str] = None,
        category_name: Optional[str] = None,
    ):
        self.vendor_id = vendor_id
        self.category_id = category_id
        self.name = name
        self.description = description
        self.address = address
        self.phone = phone
        self.website = website
        self.whatsapp = whatsapp
        self.city = city
        self.rating = rating
        self.metadata = metadata or {}
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        # Transient
        self.category_slug = category_slug
        self.category_name = category_name
    
    @classmethod
    def create(
        cls,
        category_id: int,
        name: str,
        description: str,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        website: Optional[str] = None,
        whatsapp: Optional[str] = None,
        city: Optional[str] = None,
        rating: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "ServiceVendor":
        """Factory method to create a new vendor with validation."""
        # Validate name
        if not name or len(name.strip()) < 2:
            raise InvalidVendorError("Vendor name must be at least 2 characters")
        
        # Validate description
        if not description or len(description.strip()) < 10:
            raise InvalidVendorError("Vendor description must be at least 10 characters")
        
        # Validate rating
        if rating < 0 or rating > 5:
            raise InvalidVendorError("Rating must be between 0 and 5")
        
        return cls(
            vendor_id=None,
            category_id=category_id,
            name=name.strip(),
            description=description.strip(),
            address=address.strip() if address else None,
            phone=phone.strip() if phone else None,
            website=website.strip() if website else None,
            whatsapp=whatsapp.strip() if whatsapp else None,
            city=city.strip() if city else None,
            rating=rating,
            metadata=metadata or {},
            is_active=True,
        )
    
    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        website: Optional[str] = None,
        whatsapp: Optional[str] = None,
        city: Optional[str] = None,
        rating: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
        is_active: Optional[bool] = None,
    ) -> None:
        """Update vendor details."""
        if name is not None:
            if len(name.strip()) < 2:
                raise InvalidVendorError("Vendor name must be at least 2 characters")
            self.name = name.strip()
        
        if description is not None:
            if len(description.strip()) < 10:
                raise InvalidVendorError("Vendor description must be at least 10 characters")
            self.description = description.strip()
        
        if address is not None:
            self.address = address.strip() if address else None
        
        if phone is not None:
            self.phone = phone.strip() if phone else None
        
        if website is not None:
            self.website = website.strip() if website else None
        
        if whatsapp is not None:
            self.whatsapp = whatsapp.strip() if whatsapp else None
        
        if city is not None:
            self.city = city.strip() if city else None
        
        if rating is not None:
            if rating < 0 or rating > 5:
                raise InvalidVendorError("Rating must be between 0 and 5")
            self.rating = rating
        
        if metadata is not None:
            self.metadata = metadata
        
        if is_active is not None:
            self.is_active = is_active
        
        self.updated_at = datetime.utcnow()
    
    def update_metadata(self, key: str, value: Any) -> None:
        """Update a specific metadata field."""
        self.metadata[key] = value
        self.updated_at = datetime.utcnow()
    
    def add_dish(self, name: str, category: str, image_base64: Optional[str] = None) -> None:
        """Add a dish to restaurant metadata."""
        if "dishes" not in self.metadata:
            self.metadata["dishes"] = []
        
        dish = {"name": name, "category": category}
        if image_base64:
            dish["image_base64"] = image_base64
        
        self.metadata["dishes"].append(dish)
        self.updated_at = datetime.utcnow()
    
    def remove_dish(self, dish_name: str) -> bool:
        """Remove a dish from restaurant metadata by name."""
        if "dishes" not in self.metadata:
            return False
        
        original_count = len(self.metadata["dishes"])
        self.metadata["dishes"] = [
            d for d in self.metadata["dishes"] if d.get("name") != dish_name
        ]
        
        if len(self.metadata["dishes"]) < original_count:
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def deactivate(self) -> None:
        """Soft delete - deactivate the vendor."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Reactivate the vendor."""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def __repr__(self) -> str:
        return f"ServiceVendor(id={self.vendor_id}, name={self.name}, category_id={self.category_id})"
