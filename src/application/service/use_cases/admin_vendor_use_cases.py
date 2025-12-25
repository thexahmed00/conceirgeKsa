"""Admin vendor use cases - CRUD operations."""

from src.domain.service.entities.service_vendor import ServiceVendor
from src.domain.service.repository.service_category_repository import ServiceCategoryRepository
from src.domain.service.repository.service_vendor_repository import ServiceVendorRepository
from src.domain.service.repository.vendor_image_repository import VendorImageRepository
from src.domain.shared.exceptions import ResourceNotFoundError, ValidationError
from src.application.service.dto.service_dto import (
    VendorCreateDTO,
    VendorUpdateDTO,
    VendorDetailDTO,
    VendorImageDTO,
)


class CreateVendorUseCase:
    """Create a new vendor (admin only)."""
    
    def __init__(
        self,
        category_repo: ServiceCategoryRepository,
        vendor_repo: ServiceVendorRepository,
        image_repo: VendorImageRepository,
    ):
        self.category_repo = category_repo
        self.vendor_repo = vendor_repo
        self.image_repo = image_repo
    
    def execute(self, dto: VendorCreateDTO) -> VendorDetailDTO:
        """Create a new vendor."""
        # Find category by slug
        category = self.category_repo.find_by_slug(dto.category_slug)
        if not category:
            raise ResourceNotFoundError(f"Category '{dto.category_slug}' not found")
        
        # Create vendor entity
        vendor = ServiceVendor.create(
            category_id=category.category_id,
            name=dto.name,
            description=dto.description,
            address=dto.address,
            phone=dto.phone,
            website=dto.website,
            whatsapp=dto.whatsapp,
            rating=dto.rating,
            metadata=dto.metadata,
        )
        
        # Set activation status
        if not dto.is_active:
            vendor.deactivate()
        
        # Save vendor
        saved_vendor = self.vendor_repo.save(vendor)
        
        return VendorDetailDTO(
            id=saved_vendor.vendor_id,
            category_id=saved_vendor.category_id,
            category_slug=category.slug,
            category_name=category.name,
            name=saved_vendor.name,
            description=saved_vendor.description,
            address=saved_vendor.address,
            phone=saved_vendor.phone,
            website=saved_vendor.website,
            whatsapp=saved_vendor.whatsapp,
            rating=saved_vendor.rating,
            hero_images=[],
            gallery_images=[],
            metadata=saved_vendor.metadata,
            is_active=saved_vendor.is_active,
            created_at=saved_vendor.created_at,
            updated_at=saved_vendor.updated_at,
        )


class UpdateVendorUseCase:
    """Update an existing vendor (admin only)."""
    
    def __init__(
        self,
        vendor_repo: ServiceVendorRepository,
        image_repo: VendorImageRepository,
    ):
        self.vendor_repo = vendor_repo
        self.image_repo = image_repo
    
    def execute(self, vendor_id: int, dto: VendorUpdateDTO) -> VendorDetailDTO:
        """Update vendor details."""
        # Find vendor
        vendor = self.vendor_repo.find_by_id(vendor_id)
        if not vendor:
            raise ResourceNotFoundError(f"Vendor {vendor_id} not found")
        
        # Update fields
        vendor.update(
            name=dto.name,
            description=dto.description,
            address=dto.address,
            phone=dto.phone,
            website=dto.website,
            whatsapp=dto.whatsapp,
            rating=dto.rating,
            metadata=dto.metadata,
            is_active=dto.is_active,
        )
        
        # Save updates
        updated_vendor = self.vendor_repo.update(vendor)
        
        # Get images
        hero_images = self.image_repo.find_hero_images(vendor_id)
        gallery_images = self.image_repo.find_gallery_images(vendor_id)
        
        hero_dtos = [
            VendorImageDTO(
                id=img.image_id,
                image_type=img.image_type,
                url=img.image_url,
                thumbnail_url=img.thumbnail_url,
                caption=img.caption,
                display_order=img.display_order,
            )
            for img in hero_images
        ]
        
        gallery_dtos = [
            VendorImageDTO(
                id=img.image_id,
                image_type=img.image_type,
                url=img.image_url,
                thumbnail_url=img.thumbnail_url,
                caption=img.caption,
                display_order=img.display_order,
            )
            for img in gallery_images
        ]
        
        return VendorDetailDTO(
            id=updated_vendor.vendor_id,
            category_id=updated_vendor.category_id,
            category_slug=updated_vendor.category_slug,
            category_name=updated_vendor.category_name,
            name=updated_vendor.name,
            description=updated_vendor.description,
            address=updated_vendor.address,
            phone=updated_vendor.phone,
            website=updated_vendor.website,
            whatsapp=updated_vendor.whatsapp,
            rating=updated_vendor.rating,
            hero_images=hero_dtos,
            gallery_images=gallery_dtos,
            metadata=updated_vendor.metadata,
            is_active=updated_vendor.is_active,
            created_at=updated_vendor.created_at,
            updated_at=updated_vendor.updated_at,
        )


class DeleteVendorUseCase:
    """Delete a vendor (admin only)."""
    
    def __init__(
        self,
        vendor_repo: ServiceVendorRepository,
        image_repo: VendorImageRepository,
    ):
        self.vendor_repo = vendor_repo
        self.image_repo = image_repo
    
    def execute(self, vendor_id: int, hard_delete: bool = False) -> bool:
        """
        Delete a vendor.
        
        Args:
            vendor_id: The vendor ID
            hard_delete: If True, permanently delete. If False, soft delete (deactivate).
        
        Returns:
            True if successful
        """
        vendor = self.vendor_repo.find_by_id(vendor_id)
        if not vendor:
            raise ResourceNotFoundError(f"Vendor {vendor_id} not found")
        
        if hard_delete:
            # Delete all images first (cascade should handle this, but be explicit)
            self.image_repo.delete_by_vendor_id(vendor_id)
            return self.vendor_repo.delete(vendor_id)
        else:
            # Soft delete - just deactivate
            vendor.deactivate()
            self.vendor_repo.update(vendor)
            return True
