"""Service category use cases."""

from typing import List

from src.domain.service.repository.service_category_repository import ServiceCategoryRepository
from src.application.service.dto.service_dto import (
    ServiceCategoryResponseDTO,
    ServiceCategoryListResponseDTO,
)


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
                display_order=cat.display_order,
            )
            for cat in categories
        ]
        
        return ServiceCategoryListResponseDTO(categories=category_dtos)
