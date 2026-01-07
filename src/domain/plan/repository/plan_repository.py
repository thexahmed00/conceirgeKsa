"""Plan repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.plan.entities.plan import Plan


class PlanRepository(ABC):
    """Abstract repository for Plan entities."""

    @abstractmethod
    async def find_all(self, active_only: bool = True) -> List[Plan]:
        """Find all plans."""
        pass

    @abstractmethod
    async def find_by_id(self, plan_id: int) -> Optional[Plan]:
        """Find a plan by ID."""
        pass

    @abstractmethod
    async def create(self, plan: Plan) -> Plan:
        """Create a new plan."""
        pass

    @abstractmethod
    async def update(self, plan: Plan) -> Plan:
        """Update an existing plan."""
        pass

    @abstractmethod
    async def delete(self, plan_id: int) -> bool:
        """Delete a plan by ID."""
        pass
