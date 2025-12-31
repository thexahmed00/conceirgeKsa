"""Booking DTOs for application layer."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class BookingCreateDTO(BaseModel):
    request_id: Optional[int] = None
    vendor_id: Optional[int] = None
    start_at: datetime
    end_at: Optional[datetime] = None
    notes: Optional[str] = None


class BookingResponseDTO(BaseModel):
    id: int
    request_id: int
    user_id: int
    vendor_id: Optional[int]
    start_at: datetime
    end_at: Optional[datetime]
    status: str
    notes: Optional[str]
    created_at: datetime


class BookingListResponseDTO(BaseModel):
    bookings: List[BookingResponseDTO]
    total: int
    skip: int
    limit: int
