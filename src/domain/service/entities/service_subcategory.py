"""ServiceSubcategory domain entity."""

from datetime import datetime
from typing import Optional
from src.domain.shared.exceptions import DomainException


class InvalidSubcategoryError(DomainException):
    """Raised when subcategory data is invalid."""
    pass


class ServiceSubcategory:
    """ServiceSubcategory entity - represents a sub-type of a service category."""
    
    def __init__(
        self,
        subcategory_id: Optional[int],
        category_id: int,
        slug: str,
        name: str,
        display_order: int = 0,
        icon_url: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ):
        self.subcategory_id = subcategory_id
        self.category_id = category_id
        self.slug = slug
        self.name = name
        self.display_order = display_order
        self.icon_url = icon_url
        self.created_at = created_at or datetime.utcnow()
    
    @classmethod
    def create(
        cls,
        category_id: int,
        slug: str,
        name: str,
        display_order: int = 0,
        icon_url: Optional[str] = None,
    ) -> "ServiceSubcategory":
        """Factory method to create a new subcategory with validation."""
        if not slug or len(slug.strip()) < 2:
            raise InvalidSubcategoryError("Subcategory slug must be at least 2 characters")
        
        if not name or len(name.strip()) < 2:
            raise InvalidSubcategoryError("Subcategory name must be at least 2 characters")
        
        if category_id <= 0:
            raise InvalidSubcategoryError("Category ID must be a positive integer")
        
        # Normalize slug to lowercase with underscores
        normalized_slug = slug.strip().lower().replace("-", "_").replace(" ", "_")
        
        return cls(
            subcategory_id=None,
            category_id=category_id,
            slug=normalized_slug,
            name=name.strip(),
            display_order=display_order,
            icon_url=icon_url,
        )
    
    def update(
        self,
        name: Optional[str] = None,
        display_order: Optional[int] = None,
        icon_url: Optional[str] = None,
        category_id: Optional[int] = None,
    ) -> None:
        """Update subcategory details."""
        if name is not None:
            if len(name.strip()) < 2:
                raise InvalidSubcategoryError("Subcategory name must be at least 2 characters")
            self.name = name.strip()
        
        if category_id is not None:
            if category_id <= 0:
                raise InvalidSubcategoryError("Category ID must be a positive integer")
            self.category_id = category_id
        
        if display_order is not None:
            self.display_order = display_order
        if icon_url is not None:
            self.icon_url = icon_url
    
    def __repr__(self) -> str:
        return f"ServiceSubcategory(id={self.subcategory_id}, category_id={self.category_id}, slug={self.slug}, name={self.name})"
