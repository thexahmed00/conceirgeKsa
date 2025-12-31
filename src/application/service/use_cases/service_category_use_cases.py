"""Service category use cases."""

from typing import List

from src.domain.service.repository.service_category_repository import ServiceCategoryRepository
from src.application.service.dto.service_dto import (
    ServiceCategoryResponseDTO,
    ServiceCategoryListResponseDTO,
    ServiceCategoryCreateDTO,
    ServiceCategoryUpdateDTO,
)
from src.domain.service.entities.service_category import ServiceCategory
from urllib.parse import urlparse


class ListCategoriesUseCase:
    """List all service categories."""
    
    def __init__(self, category_repo: ServiceCategoryRepository):
        self.category_repo = category_repo
    
    def execute(self) -> ServiceCategoryListResponseDTO:
        """Get all categories ordered by display_order."""
        categories = self.category_repo.find_all()
        
        category_dtos = [
            ServiceCategoryResponseDTO(
                id=cat.category_id,
                slug=cat.slug,
                name=cat.name,
                icon_url=getattr(cat, 'icon_url', None),
                display_order=cat.display_order,
            )
            for cat in categories
        ]
        
        return ServiceCategoryListResponseDTO(categories=category_dtos)


class CreateCategoryUseCase:
    """Create a new service category (admin)."""

    def __init__(self, category_repo: ServiceCategoryRepository):
        self.category_repo = category_repo

    def execute(self, dto: ServiceCategoryCreateDTO) -> ServiceCategoryResponseDTO:
        # Validate icon_url if provided
        if dto.icon_url:
            parsed = urlparse(dto.icon_url)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise ValueError("Invalid icon_url; must be a valid http/https URL")

        # Build domain entity and persist
        category = ServiceCategory.create(slug=dto.slug, name=dto.name, display_order=dto.display_order, icon_url=dto.icon_url)
        saved = self.category_repo.save(category)
        return ServiceCategoryResponseDTO(
            id=saved.category_id,
            slug=saved.slug,
            name=saved.name,
            icon_url=getattr(saved, 'icon_url', None),
            display_order=saved.display_order,
        )


class UpdateCategoryUseCase:
    """Update existing service category (admin)."""

    def __init__(self, category_repo: ServiceCategoryRepository):
        self.category_repo = category_repo

    def execute(self, category_id: int, dto: ServiceCategoryUpdateDTO) -> ServiceCategoryResponseDTO:
        existing = self.category_repo.find_by_id(category_id)
        if not existing:
            raise ValueError("Category not found")

        # Use entity update method
        existing.update(name=dto.name, display_order=dto.display_order, icon_url=dto.icon_url)
        updated = self.category_repo.update(existing)

        return ServiceCategoryResponseDTO(
            id=updated.category_id,
            slug=updated.slug,
            name=updated.name,
            icon_url=getattr(updated, 'icon_url', None),
            display_order=updated.display_order,
        )
