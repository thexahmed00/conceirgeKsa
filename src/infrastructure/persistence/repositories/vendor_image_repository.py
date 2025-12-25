"""VendorImage repository implementation."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.domain.service.entities.vendor_image import VendorImage
from src.domain.service.repository.vendor_image_repository import VendorImageRepository as IVendorImageRepository
from src.infrastructure.persistence.models.service import VendorImageModel


class VendorImageRepository(IVendorImageRepository):
    """PostgreSQL implementation of VendorImage persistence."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, image: VendorImage) -> VendorImage:
        """Save an image and return with generated ID."""
        db_image = VendorImageModel(
            vendor_id=image.vendor_id,
            image_type=image.image_type,
            image_url=image.image_url,
            thumbnail_url=image.thumbnail_url,
            caption=image.caption,
            display_order=image.display_order,
            created_at=image.created_at,
        )
        self.db.add(db_image)
        self.db.commit()
        self.db.refresh(db_image)
        
        return self._to_entity(db_image)
    
    def find_by_id(self, image_id: int) -> Optional[VendorImage]:
        """Find image by ID."""
        db_image = (
            self.db.query(VendorImageModel)
            .filter(VendorImageModel.id == image_id)
            .first()
        )
        return self._to_entity(db_image) if db_image else None
    
    def find_by_vendor_id(
        self,
        vendor_id: int,
        image_type: Optional[str] = None,
    ) -> List[VendorImage]:
        """Find all images for a vendor."""
        query = (
            self.db.query(VendorImageModel)
            .filter(VendorImageModel.vendor_id == vendor_id)
        )
        
        if image_type:
            query = query.filter(VendorImageModel.image_type == image_type)
        
        db_images = (
            query
            .order_by(VendorImageModel.display_order.asc())
            .all()
        )
        
        return [self._to_entity(img) for img in db_images]
    
    def find_hero_images(self, vendor_id: int) -> List[VendorImage]:
        """Find all hero carousel images for a vendor."""
        return self.find_by_vendor_id(vendor_id, image_type="hero")
    
    def find_gallery_images(self, vendor_id: int) -> List[VendorImage]:
        """Find all gallery images for a vendor."""
        return self.find_by_vendor_id(vendor_id, image_type="gallery")
    
    def find_first_hero_image(self, vendor_id: int) -> Optional[VendorImage]:
        """Find the first hero image for a vendor (for list thumbnails)."""
        db_image = (
            self.db.query(VendorImageModel)
            .filter(VendorImageModel.vendor_id == vendor_id)
            .filter(VendorImageModel.image_type == "hero")
            .order_by(VendorImageModel.display_order.asc())
            .first()
        )
        return self._to_entity(db_image) if db_image else None
    
    def update(self, image: VendorImage) -> VendorImage:
        """Update an existing image."""
        db_image = (
            self.db.query(VendorImageModel)
            .filter(VendorImageModel.id == image.image_id)
            .first()
        )
        
        if db_image:
            db_image.caption = image.caption
            db_image.display_order = image.display_order
            self.db.commit()
            self.db.refresh(db_image)
            return self._to_entity(db_image)
        
        return image
    
    def delete(self, image_id: int) -> bool:
        """Delete an image by ID."""
        db_image = (
            self.db.query(VendorImageModel)
            .filter(VendorImageModel.id == image_id)
            .first()
        )
        
        if db_image:
            self.db.delete(db_image)
            self.db.commit()
            return True
        
        return False
    
    def delete_by_vendor_id(self, vendor_id: int) -> int:
        """Delete all images for a vendor.

        Raises:
            ValueError: If no images were found for the given vendor_id.
        """
        count = (
            self.db.query(VendorImageModel)
            .filter(VendorImageModel.vendor_id == vendor_id)
            .delete()
        )
        self.db.commit()

        if count == 0:
            raise ValueError(f"No images found for vendor_id={vendor_id}")
        return count
    
    def reorder(self, vendor_id: int, image_type: str, image_ids: List[int]) -> bool:
        """Reorder images by setting display_order based on position in image_ids list."""
        try:
            for order, image_id in enumerate(image_ids):
                db_image = (
                    self.db.query(VendorImageModel)
                    .filter(VendorImageModel.id == image_id)
                    .filter(VendorImageModel.vendor_id == vendor_id)
                    .filter(VendorImageModel.image_type == image_type)
                    .first()
                )
                if db_image:
                    db_image.display_order = order
            
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False
    
    def get_next_display_order(self, vendor_id: int, image_type: str) -> int:
        """Get the next display_order value for a new image."""
        max_order = (
            self.db.query(func.max(VendorImageModel.display_order))
            .filter(VendorImageModel.vendor_id == vendor_id)
            .filter(VendorImageModel.image_type == image_type)
            .scalar()
        )
        return (max_order or 0) + 1
    
    def _to_entity(self, model: VendorImageModel) -> VendorImage:
        """Convert ORM model to domain entity."""
        return VendorImage(
            image_id=model.id,
            vendor_id=model.vendor_id,
            image_type=model.image_type,
            image_url=model.image_url,
            thumbnail_url=model.thumbnail_url,
            caption=model.caption,
            display_order=model.display_order,
            created_at=model.created_at,
        )
