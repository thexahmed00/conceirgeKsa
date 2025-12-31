"""Service vendor use cases - user-facing operations."""

from typing import List, Optional

from src.domain.service.repository.service_vendor_repository import ServiceVendorRepository
from src.domain.service.repository.vendor_image_repository import VendorImageRepository
from src.domain.shared.exceptions import ResourceNotFoundError
from src.application.service.dto.service_dto import (
    VendorListItemDTO,
    VendorListResponseDTO,
    VendorDetailDTO,
    VendorImageDTO,
)


class ListVendorsByCategoryUseCase:
    """List all vendors."""
    
    def __init__(
        self,
        vendor_repo: ServiceVendorRepository,
        image_repo: VendorImageRepository,
    ):
        self.vendor_repo = vendor_repo
        self.image_repo = image_repo
    
    def execute(
        self,
        category_slug: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> VendorListResponseDTO:
        """Get vendors for a category with pagination. If category_slug is None, list all vendors."""
        if category_slug:
            vendors, total = self.vendor_repo.find_by_category_slug(
                category_slug=category_slug,
                skip=skip,
                limit=limit,
                active_only=True,
            )
        else:
            vendors, total = self.vendor_repo.find_all(
                skip=skip,
                limit=limit,
                active_only=True,
            )

        vendor_dtos = []
        for vendor in vendors:
            # Get first hero image and use its direct image URL as the list hero URL
            first_hero = self.image_repo.find_first_hero_image(vendor.vendor_id)
            hero_url = first_hero.image_url if first_hero else None

            # Truncate description for list view
            short_desc = vendor.description[:150] + "..." if len(vendor.description) > 150 else vendor.description

            vendor_dtos.append(
                VendorListItemDTO(
                    id=vendor.vendor_id,
                    name=vendor.name,
                    category_slug=vendor.category_slug,
                    category_name=vendor.category_name,
                    thumbnail_url=hero_url,
                    rating=vendor.rating,
                    short_description=short_desc,
                    address=vendor.address,
                )
            )

        return VendorListResponseDTO(
            vendors=vendor_dtos,
            total=total,
            skip=skip,
            limit=limit,
        )


class GetVendorDetailUseCase:
    """Get full details for a specific vendor."""
    
    def __init__(
        self,
        vendor_repo: ServiceVendorRepository,
        image_repo: VendorImageRepository,
    ):
        self.vendor_repo = vendor_repo
        self.image_repo = image_repo
    
    def execute(self, vendor_id: int) -> VendorDetailDTO:
        """Get vendor details including images and metadata."""
        vendor = self.vendor_repo.find_by_id(vendor_id)
        
        if not vendor:
            raise ResourceNotFoundError(f"Vendor {vendor_id} not found")
        
        # Get hero images
        hero_images = self.image_repo.find_hero_images(vendor_id)
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
        
        # Get gallery images
        gallery_images = self.image_repo.find_gallery_images(vendor_id)
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
            id=vendor.vendor_id,
            category_id=vendor.category_id,
            category_slug=vendor.category_slug,
            category_name=vendor.category_name,
            name=vendor.name,
            description=vendor.description,
            address=vendor.address,
            phone=vendor.phone,
            website=vendor.website,
            whatsapp=vendor.whatsapp,
            rating=vendor.rating,
            hero_images=hero_dtos,
            gallery_images=gallery_dtos,
            metadata=vendor.metadata,
            is_active=vendor.is_active,
            created_at=vendor.created_at,
            updated_at=vendor.updated_at,
        )
