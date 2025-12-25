"""ServiceCategory repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.service.entities.service_category import ServiceCategory


class ServiceCategoryRepository(ABC):
    """Abstract repository for ServiceCategory persistence."""
    
    @abstractmethod
    def save(self, category: ServiceCategory) -> ServiceCategory:
        """Save a category and return with generated ID."""
        pass
    
    @abstractmethod
    def find_by_id(self, category_id: int) -> Optional[ServiceCategory]:
        """Find category by ID."""
        pass
    
    @abstractmethod
    def find_by_slug(self, slug: str) -> Optional[ServiceCategory]:
        """Find category by slug."""
        pass
    
    @abstractmethod
    def find_all(self) -> List[ServiceCategory]:
        """Find all categories ordered by display_order."""
        pass
    
    @abstractmethod
    def update(self, category: ServiceCategory) -> ServiceCategory:
        """Update an existing category."""
        pass
    
    @abstractmethod
    def delete(self, category_id: int) -> bool:
        """Delete a category by ID."""
        pass
