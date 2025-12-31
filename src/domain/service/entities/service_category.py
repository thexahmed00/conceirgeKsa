"""ServiceCategory domain entity."""

from datetime import datetime
from typing import Optional
from src.domain.shared.exceptions import DomainException


class InvalidCategoryError(DomainException):
    """Raised when category data is invalid."""
    pass


class ServiceCategory:
    """ServiceCategory entity - represents a type of concierge service."""
    
    # Predefined category slugs
    VALID_SLUGS = ["restaurant", "private_jet", "flight", "car", "hotel", "car_driver"]
    
    def __init__(
        self,
        category_id: Optional[int],
        slug: str,
        name: str,
        display_order: int = 0,
        icon_url: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ):
        self.category_id = category_id
        self.slug = slug
        self.name = name
        self.display_order = display_order
        self.icon_url = icon_url
        self.created_at = created_at or datetime.utcnow()
    
    @classmethod
    def create(cls, slug: str, name: str, display_order: int = 0, icon_url: Optional[str] = None) -> "ServiceCategory":
        """Factory method to create a new category with validation."""
        if not slug or len(slug.strip()) < 2:
            raise InvalidCategoryError("Category slug must be at least 2 characters")
        
        if not name or len(name.strip()) < 2:
            raise InvalidCategoryError("Category name must be at least 2 characters")
        
        # Normalize slug to lowercase with underscores
        normalized_slug = slug.strip().lower().replace("-", "_").replace(" ", "_")
        
        return cls(
            category_id=None,
            slug=normalized_slug,
            name=name.strip(),
            display_order=display_order,
            icon_url=icon_url,
        )
    
    def update(self, name: Optional[str] = None, display_order: Optional[int] = None, icon_url: Optional[str] = None) -> None:
        """Update category details."""
        if name is not None:
            if len(name.strip()) < 2:
                raise InvalidCategoryError("Category name must be at least 2 characters")
            self.name = name.strip()
        
        if display_order is not None:
            self.display_order = display_order
        if icon_url is not None:
            self.icon_url = icon_url
    
    def __repr__(self) -> str:
        return f"ServiceCategory(id={self.category_id}, slug={self.slug}, name={self.name}, icon={self.icon_url})"
