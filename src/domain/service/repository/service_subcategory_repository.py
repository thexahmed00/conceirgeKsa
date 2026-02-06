"""ServiceSubcategory repository interface."""

from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.service.entities.service_subcategory import ServiceSubcategory


class ServiceSubcategoryRepository(ABC):
    """Abstract repository for ServiceSubcategory persistence."""
    
    @abstractmethod
    def save(self, subcategory: ServiceSubcategory) -> ServiceSubcategory:
        """Save a subcategory and return with generated ID."""
        pass
    
    @abstractmethod
    def find_by_id(self, subcategory_id: int) -> Optional[ServiceSubcategory]:
        """Find subcategory by ID."""
        pass
    
    @abstractmethod
    def find_by_slug(self, slug: str) -> Optional[ServiceSubcategory]:
        """Find subcategory by slug."""
        pass
    
    @abstractmethod
    def find_by_category_id(self, category_id: int) -> List[ServiceSubcategory]:
        """Find all subcategories for a given category."""
        pass
    
    @abstractmethod
    def find_all(self) -> List[ServiceSubcategory]:
        """Find all subcategories."""
        pass
    
    @abstractmethod
    def update(self, subcategory: ServiceSubcategory) -> ServiceSubcategory:
        """Update an existing subcategory."""
        pass
    
    @abstractmethod
    def delete(self, subcategory_id: int) -> bool:
        """Delete a subcategory by ID. Returns True if successful."""
        pass
