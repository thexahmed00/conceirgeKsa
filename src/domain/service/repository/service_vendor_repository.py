"""ServiceVendor repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from src.domain.service.entities.service_vendor import ServiceVendor


class ServiceVendorRepository(ABC):
    """Abstract repository for ServiceVendor persistence."""
    
    @abstractmethod
    def save(self, vendor: ServiceVendor) -> ServiceVendor:
        """Save a vendor and return with generated ID."""
        pass
    
    @abstractmethod
    def find_by_id(self, vendor_id: int) -> Optional[ServiceVendor]:
        """Find vendor by ID."""
        pass
    
    @abstractmethod
    def find_by_category_id(
        self,
        category_id: int,
        skip: int = 0,
        limit: int = 20,
        active_only: bool = True,
    ) -> Tuple[List[ServiceVendor], int]:
        """Find all vendors for a category with pagination. Returns (vendors, total_count)."""
        pass
    
    @abstractmethod
    def find_by_category_slug(
        self,
        category_slug: str,
        skip: int = 0,
        limit: int = 20,
        active_only: bool = True,
    ) -> Tuple[List[ServiceVendor], int]:
        """Find all vendors for a category by slug with pagination. Returns (vendors, total_count)."""
        pass
    
    @abstractmethod
    def find_all(
        self,
        skip: int = 0,
        limit: int = 20,
        active_only: bool = True,
    ) -> Tuple[List[ServiceVendor], int]:
        """Find all vendors with pagination. Returns (vendors, total_count)."""
        pass
    
    @abstractmethod
    def update(self, vendor: ServiceVendor) -> ServiceVendor:
        """Update an existing vendor."""
        pass
    
    @abstractmethod
    def delete(self, vendor_id: int) -> bool:
        """Hard delete a vendor by ID."""
        pass
    
    @abstractmethod
    def count_by_category(self, category_id: int, active_only: bool = True) -> int:
        """Count vendors in a category."""
        pass
