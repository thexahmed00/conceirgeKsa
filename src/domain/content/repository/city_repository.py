"""City repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.content.entities.city import City


class CityRepository(ABC):
    """Abstract repository for City entities."""

    @abstractmethod
    async def find_all(self, active_only: bool = True) -> List[City]:
        """Find all cities."""
        pass

    @abstractmethod
    async def find_by_id(self, city_id: int) -> Optional[City]:
        """Find a city by ID."""
        pass

    @abstractmethod
    async def create(self, city: City) -> City:
        """Create a new city."""
        pass

    @abstractmethod
    async def update(self, city: City) -> City:
        """Update an existing city."""
        pass

    @abstractmethod
    async def delete(self, city_id: int) -> bool:
        """Delete a city by ID."""
        pass
