"""VendorImage domain entity."""

from datetime import datetime
from typing import Optional
from urllib.parse import urlparse
from src.domain.shared.exceptions import DomainException


class InvalidImageError(DomainException):
    """Raised when image data is invalid."""
    pass


def _validate_url(url: str) -> bool:
    """Validate URL format and scheme."""
    if not url:
        return False
    try:
        parsed = urlparse(url)
        # Must have valid scheme and netloc (domain)
        if parsed.scheme not in ("http", "https"):
            return False
        if not parsed.netloc:
            return False
        # Basic domain validation - must have at least one dot or be localhost
        if "." not in parsed.netloc and "localhost" not in parsed.netloc:
            return False
        return True
    except Exception:
        return False


class VendorImage:
    """VendorImage entity - represents hero carousel or gallery images for a vendor."""
    
    VALID_IMAGE_TYPES = ["hero", "gallery"]
    
    def __init__(
        self,
        image_id: Optional[int],
        vendor_id: int,
        image_type: str,
        image_url: str,
        thumbnail_url: Optional[str] = None,
        caption: Optional[str] = None,
        display_order: int = 0,
        created_at: Optional[datetime] = None,
    ):
        self.image_id = image_id
        self.vendor_id = vendor_id
        self.image_type = image_type
        self.image_url = image_url
        self.thumbnail_url = thumbnail_url
        self.caption = caption
        self.display_order = display_order
        self.created_at = created_at or datetime.utcnow()
    
    @classmethod
    def create(
        cls,
        vendor_id: int,
        image_type: str,
        image_url: str,
        thumbnail_url: Optional[str] = None,
        caption: Optional[str] = None,
        display_order: int = 0,
    ) -> "VendorImage":
        """Factory method to create a new vendor image with validation."""
        # Validate image type
        if image_type not in cls.VALID_IMAGE_TYPES:
            raise InvalidImageError(
                f"Invalid image type: {image_type}. Must be one of {cls.VALID_IMAGE_TYPES}"
            )
        
        # Validate URL format
        if not _validate_url(image_url):
            raise InvalidImageError(
                "image_url must be a valid HTTP/HTTPS URL with a proper domain"
            )
        
        # Validate thumbnail URL if provided
        if thumbnail_url and not _validate_url(thumbnail_url):
            raise InvalidImageError(
                "thumbnail_url must be a valid HTTP/HTTPS URL with a proper domain"
            )
        
        return cls(
            image_id=None,
            vendor_id=vendor_id,
            image_type=image_type,
            image_url=image_url,
            thumbnail_url=thumbnail_url,
            caption=caption.strip() if caption else None,
            display_order=display_order,
        )
    
    def update(
        self,
        caption: Optional[str] = None,
        display_order: Optional[int] = None,
    ) -> None:
        """Update image metadata."""
        if caption is not None:
            self.caption = caption.strip() if caption else None
        
        if display_order is not None:
            self.display_order = display_order
    
    @property
    def is_hero(self) -> bool:
        """Check if this is a hero carousel image."""
        return self.image_type == "hero"
    
    @property
    def is_gallery(self) -> bool:
        """Check if this is a gallery image."""
        return self.image_type == "gallery"
    
    def __repr__(self) -> str:
        return f"VendorImage(id={self.image_id}, vendor_id={self.vendor_id}, type={self.image_type})"
