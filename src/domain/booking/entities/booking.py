"""Booking domain entity."""

from datetime import datetime
from typing import Optional
from src.domain.shared.exceptions import DomainException


class InvalidBookingError(DomainException):
    pass


class Booking:
    """Booking aggregate representing a confirmed booking."""

    VALID_STATUSES = ["upcoming", "completed", "cancelled"]

    def __init__(
        self,
        booking_id: Optional[int],
        request_id: int,
        user_id: int,
        vendor_id: Optional[int],
        start_at: datetime,
        end_at: Optional[datetime],
        status: str = "upcoming",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        created_by: Optional[int] = None,
    ):
        self.booking_id = booking_id
        self.request_id = request_id
        self.user_id = user_id
        self.vendor_id = vendor_id
        self.start_at = start_at
        self.end_at = end_at
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.utcnow()
        self.created_by = created_by

    @classmethod
    def create(
        cls,
        request_id: int,
        user_id: int,
        vendor_id: Optional[int],
        start_at: datetime,
        end_at: Optional[datetime] = None,
        created_by: Optional[int] = None,
        notes: Optional[str] = None,
    ) -> "Booking":
        if start_at is None:
            raise InvalidBookingError("start_at is required for a booking")

        return cls(
            booking_id=None,
            request_id=request_id,
            user_id=user_id,
            vendor_id=vendor_id,
            start_at=start_at,
            end_at=end_at,
            status="upcoming",
            notes=notes,
            created_by=created_by,
        )

    def complete(self) -> None:
        if self.status != "upcoming":
            raise InvalidBookingError("Only upcoming bookings can be completed")
        self.status = "completed"

    def cancel(self) -> None:
        if self.status == "completed":
            raise InvalidBookingError("Cannot cancel a completed booking")
        self.status = "cancelled"

    def __repr__(self) -> str:
        return f"Booking(id={self.booking_id}, request={self.request_id}, status={self.status})"
