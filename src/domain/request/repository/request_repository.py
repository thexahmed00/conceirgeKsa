"""Request repository interface (domain layer)."""

from __future__ import annotations

from typing import List, Optional, Protocol

from src.domain.request.entities.request import Request


class RequestRepository(Protocol):
    def save(self, request: Request) -> Request:
        ...

    def find_by_id(self, request_id: int) -> Optional[Request]:
        ...

    def find_by_user_id(self, user_id: int, skip: int = 0, limit: int = 20) -> List[Request]:
        ...

    def update(self, request: Request) -> Request:
        ...
