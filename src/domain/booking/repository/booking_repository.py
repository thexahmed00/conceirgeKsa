"""Booking repository interface (domain layer)."""

from __future__ import annotations

from typing import List, Optional, Protocol

from src.domain.booking.entities.booking import Booking


class BookingRepository(Protocol):
    def save(self, booking: Booking) -> Booking:
        ...

    def find_by_id(self, booking_id: int) -> Optional[Booking]:
        ...

    def find_by_user_and_status(self, user_id: int, status: Optional[str] = None, skip: int = 0, limit: int = 20) -> List[Booking]:
        ...

    def count_by_user_and_status(self, user_id: int, status: Optional[str] = None) -> int:
        ...

    def find_all(self, status: Optional[str] = None, skip: int = 0, limit: int = 20) -> List[Booking]:
        ...

    def count_all(self, status: Optional[str] = None) -> int:
        ...

    def update(self, booking: Booking) -> Booking:
        ...
