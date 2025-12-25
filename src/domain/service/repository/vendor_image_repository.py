"""VendorImage repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.service.entities.vendor_image import VendorImage


class VendorImageRepository(ABC):
    """Abstract repository for VendorImage persistence."""
    
    @abstractmethod
    def save(self, image: VendorImage) -> VendorImage:
        """Save an image and return with generated ID."""
        pass
    
    @abstractmethod
    def find_by_id(self, image_id: int) -> Optional[VendorImage]:
        """Find image by ID."""
        pass
    
    @abstractmethod
    def find_by_vendor_id(
        self,
        vendor_id: int,
        image_type: Optional[str] = None,
    ) -> List[VendorImage]:
        """
        Find all images for a vendor.
        
        Args:
            vendor_id: The vendor ID
            image_type: Optional filter - 'hero', 'gallery', or None for all
        
        Returns:
            List of images ordered by display_order
        """
        pass
    
    @abstractmethod
    def find_hero_images(self, vendor_id: int) -> List[VendorImage]:
        """Find all hero carousel images for a vendor."""
        pass
    
    @abstractmethod
    def find_gallery_images(self, vendor_id: int) -> List[VendorImage]:
        """Find all gallery images for a vendor."""
        pass
    
    @abstractmethod
    def find_first_hero_image(self, vendor_id: int) -> Optional[VendorImage]:
        """Find the first hero image for a vendor (for list thumbnails)."""
        pass
    
    @abstractmethod
    def update(self, image: VendorImage) -> VendorImage:
        """Update an existing image."""
        pass
    
    @abstractmethod
    def delete(self, image_id: int) -> bool:
        """Delete an image by ID."""
        pass
    
    @abstractmethod
    def delete_by_vendor_id(self, vendor_id: int) -> int:
        """Delete all images for a vendor. Returns count of deleted images."""
        pass
    
    @abstractmethod
    def reorder(self, vendor_id: int, image_type: str, image_ids: List[int]) -> bool:
        """
        Reorder images by setting display_order based on position in image_ids list.
        
        Args:
            vendor_id: The vendor ID
            image_type: 'hero' or 'gallery'
            image_ids: List of image IDs in desired order
        
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    def get_next_display_order(self, vendor_id: int, image_type: str) -> int:
        """Get the next display_order value for a new image."""
        pass
