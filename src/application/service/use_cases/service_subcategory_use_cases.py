"""Use cases for managing service subcategories."""

from typing import List
from src.domain.service.entities.service_subcategory import ServiceSubcategory, InvalidSubcategoryError
from src.domain.service.repository.service_subcategory_repository import ServiceSubcategoryRepository
from src.domain.service.repository.service_category_repository import ServiceCategoryRepository
from src.application.service.dto.service_dto import (
    ServiceSubcategoryResponseDTO,
    ServiceSubcategoryCreateDTO,
    ServiceSubcategoryUpdateDTO,
    ServiceSubcategoryListResponseDTO,
)


class CreateSubcategoryUseCase:
    """Create a new service subcategory."""
    
    def __init__(
        self,
        subcategory_repo: ServiceSubcategoryRepository,
        category_repo: ServiceCategoryRepository,
    ):
        self.subcategory_repo = subcategory_repo
        self.category_repo = category_repo
    
    def execute(self, dto: ServiceSubcategoryCreateDTO) -> ServiceSubcategoryResponseDTO:
        """Create and save a new subcategory."""
        # Verify category exists
        category = self.category_repo.find_by_id(dto.category_id)
        if not category:
            raise ValueError(f"Category with ID {dto.category_id} not found")
        
        # Create entity with validation
        try:
            subcategory = ServiceSubcategory.create(
                category_id=dto.category_id,
                slug=dto.slug,
                name=dto.name,
                display_order=dto.display_order,
                icon_url=dto.icon_url,
            )
        except InvalidSubcategoryError as e:
            raise ValueError(str(e))
        
        # Save to repository
        saved = self.subcategory_repo.save(subcategory)
        
        return ServiceSubcategoryResponseDTO(
            id=saved.subcategory_id,
            category_id=saved.category_id,
            slug=saved.slug,
            name=saved.name,
            icon_url=saved.icon_url,
            display_order=saved.display_order,
        )


class UpdateSubcategoryUseCase:
    """Update an existing service subcategory."""
    
    def __init__(self, subcategory_repo: ServiceSubcategoryRepository):
        self.subcategory_repo = subcategory_repo
    
    def execute(
        self,
        subcategory_id: int,
        dto: ServiceSubcategoryUpdateDTO,
    ) -> ServiceSubcategoryResponseDTO:
        """Update a subcategory."""
        subcategory = self.subcategory_repo.find_by_id(subcategory_id)
        if not subcategory:
            raise ValueError(f"Subcategory with ID {subcategory_id} not found")
        
        try:
            subcategory.update(
                name=dto.name,
                display_order=dto.display_order,
                icon_url=dto.icon_url,
            )
        except InvalidSubcategoryError as e:
            raise ValueError(str(e))
        
        updated = self.subcategory_repo.update(subcategory)
        
        return ServiceSubcategoryResponseDTO(
            id=updated.subcategory_id,
            category_id=updated.category_id,
            slug=updated.slug,
            name=updated.name,
            icon_url=updated.icon_url,
            display_order=updated.display_order,
        )


class GetSubcategoryUseCase:
    """Get a specific subcategory by ID."""
    
    def __init__(self, subcategory_repo: ServiceSubcategoryRepository):
        self.subcategory_repo = subcategory_repo
    
    def execute(self, subcategory_id: int) -> ServiceSubcategoryResponseDTO:
        """Retrieve a subcategory by ID."""
        subcategory = self.subcategory_repo.find_by_id(subcategory_id)
        if not subcategory:
            raise ValueError(f"Subcategory with ID {subcategory_id} not found")
        
        return ServiceSubcategoryResponseDTO(
            id=subcategory.subcategory_id,
            category_id=subcategory.category_id,
            slug=subcategory.slug,
            name=subcategory.name,
            icon_url=subcategory.icon_url,
            display_order=subcategory.display_order,
        )


class ListSubcategoriesByCategoryUseCase:
    """List all subcategories for a specific category."""
    
    def __init__(self, subcategory_repo: ServiceSubcategoryRepository):
        self.subcategory_repo = subcategory_repo
    
    def execute(self, category_id: int) -> ServiceSubcategoryListResponseDTO:
        """Get all subcategories for a category."""
        subcategories = self.subcategory_repo.find_by_category_id(category_id)
        
        return ServiceSubcategoryListResponseDTO(
            subcategories=[
                ServiceSubcategoryResponseDTO(
                    id=sc.subcategory_id,
                    category_id=sc.category_id,
                    slug=sc.slug,
                    name=sc.name,
                    icon_url=sc.icon_url,
                    display_order=sc.display_order,
                )
                for sc in subcategories
            ]
        )


class ListAllSubcategoriesUseCase:
    """List all subcategories."""
    
    def __init__(self, subcategory_repo: ServiceSubcategoryRepository):
        self.subcategory_repo = subcategory_repo
    
    def execute(self) -> ServiceSubcategoryListResponseDTO:
        """Get all subcategories."""
        subcategories = self.subcategory_repo.find_all()
        
        return ServiceSubcategoryListResponseDTO(
            subcategories=[
                ServiceSubcategoryResponseDTO(
                    id=sc.subcategory_id,
                    category_id=sc.category_id,
                    slug=sc.slug,
                    name=sc.name,
                    icon_url=sc.icon_url,
                    display_order=sc.display_order,
                )
                for sc in subcategories
            ]
        )


class DeleteSubcategoryUseCase:
    """Delete a service subcategory."""
    
    def __init__(self, subcategory_repo: ServiceSubcategoryRepository):
        self.subcategory_repo = subcategory_repo
    
    def execute(self, subcategory_id: int) -> bool:
        """Delete a subcategory."""
        return self.subcategory_repo.delete(subcategory_id)
