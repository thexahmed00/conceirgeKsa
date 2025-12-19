"""User repository interface (domain layer).

Defines the persistence contract required by application use cases.
"""

from __future__ import annotations

from typing import Optional, Protocol

from src.domain.user.entities.user import User


class UserRepository(Protocol):
    async def save(self, user: User) -> User:
        ...

    async def find_by_id(self, user_id: int) -> Optional[User]:
        ...

    async def find_by_email(self, email: str) -> Optional[User]:
        ...

    async def update(self, user: User) -> User:
        ...
