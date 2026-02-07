"""Service category use cases."""

from typing import List

from src.domain.service.repository.service_category_repository import ServiceCategoryRepository
from src.domain.service.repository.service_subcategory_repository import ServiceSubcategoryRepository
from src.application.service.dto.service_dto import (
    ServiceCategoryResponseDTO,
    ServiceCategoryListResponseDTO,
    ServiceCategoryCreateDTO,
    ServiceCategoryUpdateDTO,
    ServiceCategoryWithSubcategoriesDTO,
    ServiceCategoryWithSubcategoriesListResponseDTO,
    ServiceSubcategoryResponseDTO,
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


class ListCategoriesWithSubcategoriesUseCase:
    """List all service categories with their subcategories."""

    def __init__(self, category_repo: ServiceCategoryRepository):
        self.category_repo = category_repo

    def execute(self) -> ServiceCategoryWithSubcategoriesListResponseDTO:
        """Get all categories with nested subcategories."""
        items = self.category_repo.find_all_with_subcategories()

        category_dtos = [
            ServiceCategoryWithSubcategoriesDTO(
                id=item["category"].category_id,
                slug=item["category"].slug,
                name=item["category"].name,
                icon_url=getattr(item["category"], "icon_url", None),
                display_order=item["category"].display_order,
                subcategories=[
                    ServiceSubcategoryResponseDTO(
                        id=sc.subcategory_id,
                        category_id=sc.category_id,
                        slug=sc.slug,
                        name=sc.name,
                        icon_url=sc.icon_url,
                        display_order=sc.display_order,
                    )
                    for sc in item["subcategories"]
                ],
            )
            for item in items
        ]

        return ServiceCategoryWithSubcategoriesListResponseDTO(categories=category_dtos)


class CreateCategoryUseCase:
    """Create a new service category (admin)."""

    def __init__(
        self,
        category_repo: ServiceCategoryRepository,
        subcategory_repo: ServiceSubcategoryRepository,
    ):
        self.category_repo = category_repo
        self.subcategory_repo = subcategory_repo

    def execute(self, dto: ServiceCategoryCreateDTO) -> ServiceCategoryWithSubcategoriesDTO:
        # Validate icon_url if provided
        if dto.icon_url:
            parsed = urlparse(dto.icon_url)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise ValueError("Invalid icon_url; must be a valid http/https URL")

        # Build domain entity and persist
        category = ServiceCategory.create(slug=dto.slug, name=dto.name, display_order=dto.display_order, icon_url=dto.icon_url)
        saved = self.category_repo.save(category)

        # Reassign selected subcategories to this new category
        attached_subcategories = []
        if dto.subcategory_ids:
            for sc_id in dto.subcategory_ids:
                sc = self.subcategory_repo.find_by_id(sc_id)
                if not sc:
                    raise ValueError(f"Subcategory with ID {sc_id} not found")
                sc.update(category_id=saved.category_id)
                updated_sc = self.subcategory_repo.update(sc)
                attached_subcategories.append(updated_sc)

        return ServiceCategoryWithSubcategoriesDTO(
            id=saved.category_id,
            slug=saved.slug,
            name=saved.name,
            icon_url=getattr(saved, 'icon_url', None),
            display_order=saved.display_order,
            subcategories=[
                ServiceSubcategoryResponseDTO(
                    id=sc.subcategory_id,
                    category_id=sc.category_id,
                    slug=sc.slug,
                    name=sc.name,
                    icon_url=sc.icon_url,
                    display_order=sc.display_order,
                )
                for sc in attached_subcategories
            ],
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
