"""Vendor image use cases."""

from src.domain.service.entities.vendor_image import VendorImage
from src.domain.service.repository.service_vendor_repository import ServiceVendorRepository
from src.domain.service.repository.vendor_image_repository import VendorImageRepository
from src.domain.shared.exceptions import ResourceNotFoundError, ValidationError, AccessDeniedError
from src.application.service.dto.service_dto import (
    ImageCreateDTO,
    ImageReorderDTO,
    VendorImageDTO,
)


class AddVendorImageUseCase:
    """Add an image to a vendor (hero or gallery)."""
    
    def __init__(
        self,
        vendor_repo: ServiceVendorRepository,
        image_repo: VendorImageRepository,
    ):
        self.vendor_repo = vendor_repo
        self.image_repo = image_repo
    
    def execute(self, vendor_id: int, dto: ImageCreateDTO) -> VendorImageDTO:
        """Add a new image to the vendor."""
        # Verify vendor exists
        vendor = self.vendor_repo.find_by_id(vendor_id)
        if not vendor:
            raise ResourceNotFoundError(f"Vendor {vendor_id} not found")
        
        # Validate image type
        if dto.image_type not in VendorImage.VALID_IMAGE_TYPES:
            raise ValidationError(
                f"Invalid image type: {dto.image_type}. Must be one of {VendorImage.VALID_IMAGE_TYPES}"
            )
        
        # Get next display order
        display_order = self.image_repo.get_next_display_order(vendor_id, dto.image_type)
        
        # Create image entity
        image = VendorImage.create(
            vendor_id=vendor_id,
            image_type=dto.image_type,
            image_url=dto.image_url,
            thumbnail_url=dto.thumbnail_url,
            caption=dto.caption,
            display_order=display_order,
        )
        
        # Save image
        saved_image = self.image_repo.save(image)
        
        return VendorImageDTO(
            id=saved_image.image_id,
            image_type=saved_image.image_type,
            url=saved_image.image_url,
            thumbnail_url=saved_image.thumbnail_url,
            caption=saved_image.caption,
            display_order=saved_image.display_order,
        )


class DeleteVendorImageUseCase:
    """Delete a vendor image."""
    
    def __init__(
        self,
        vendor_repo: ServiceVendorRepository,
        image_repo: VendorImageRepository,
    ):
        self.vendor_repo = vendor_repo
        self.image_repo = image_repo
    
    def execute(self, vendor_id: int, image_id: int) -> bool:
        """Delete an image from the vendor."""
        # Verify vendor exists
        vendor = self.vendor_repo.find_by_id(vendor_id)
        if not vendor:
            raise ResourceNotFoundError(f"Vendor {vendor_id} not found")
        
        # Verify image exists and belongs to vendor
        image = self.image_repo.find_by_id(image_id)
        if not image:
            raise ResourceNotFoundError(f"Image {image_id} not found")
        
        if image.vendor_id != vendor_id:
            raise AccessDeniedError("Image does not belong to this vendor")
        
        return self.image_repo.delete(image_id)


class ReorderVendorImagesUseCase:
    """Reorder vendor images."""
    
    def __init__(
        self,
        vendor_repo: ServiceVendorRepository,
        image_repo: VendorImageRepository,
    ):
        self.vendor_repo = vendor_repo
        self.image_repo = image_repo
    
    def execute(
        self,
        vendor_id: int,
        image_type: str,
        dto: ImageReorderDTO,
    ) -> bool:
        """Reorder images of a specific type."""
        # Verify vendor exists
        vendor = self.vendor_repo.find_by_id(vendor_id)
        if not vendor:
            raise ResourceNotFoundError(f"Vendor {vendor_id} not found")
        
        # Validate image type
        if image_type not in VendorImage.VALID_IMAGE_TYPES:
            raise ValidationError(
                f"Invalid image type: {image_type}. Must be one of {VendorImage.VALID_IMAGE_TYPES}"
            )
        
        return self.image_repo.reorder(vendor_id, image_type, dto.image_ids)


class GetVendorImageUseCase:
    """Get image info."""
    
    def __init__(self, image_repo: VendorImageRepository):
        self.image_repo = image_repo
    
    def execute(self, image_id: int) -> VendorImageDTO:
        """Get image info."""
        image = self.image_repo.find_by_id(image_id)
        if not image:
            raise ResourceNotFoundError(f"Image {image_id} not found")
        
        return VendorImageDTO(
            id=image.image_id,
            image_type=image.image_type,
            url=image.image_url,
            thumbnail_url=image.thumbnail_url,
            caption=image.caption,
            display_order=image.display_order,
        )
