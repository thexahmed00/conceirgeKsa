"""Banner repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.content.entities.banner import Banner


class BannerRepository(ABC):
    """Abstract repository for Banner entities."""

    @abstractmethod
    async def find_all(self, active_only: bool = True) -> List[Banner]:
        """Find all banners."""
        pass

    @abstractmethod
    async def find_by_id(self, banner_id: int) -> Optional[Banner]:
        """Find a banner by ID."""
        pass

    @abstractmethod
    async def create(self, banner: Banner) -> Banner:
        """Create a new banner."""
        pass

    @abstractmethod
    async def update(self, banner: Banner) -> Banner:
        """Update an existing banner."""
        pass

    @abstractmethod
    async def delete(self, banner_id: int) -> bool:
        """Delete a banner by ID."""
        pass
