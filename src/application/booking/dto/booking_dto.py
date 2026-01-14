"""Booking DTOs for application layer."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class BookingCreateDTO(BaseModel):
    """Full booking creation DTO (requires all IDs)."""
    request_id: int
    vendor_id: Optional[int] = None
    start_at: datetime
    end_at: Optional[datetime] = None
    notes: Optional[str] = None


class BookingConfirmDTO(BaseModel):
    """Simplified DTO for confirming a conversation and creating a booking.
    
    Only requires booking times - request_id and vendor_id are resolved 
    from the conversation automatically.
    """
    start_at: datetime = Field(..., description="Booking start date/time")
    end_at: Optional[datetime] = Field(None, description="Booking end date/time (optional)")
    notes: Optional[str] = Field(None, description="Additional notes for the booking")
    
    class Config:
        json_schema_extra = {
            "example": {
                "start_at": "2026-01-20T14:00:00Z",
                "end_at": "2026-01-20T16:00:00Z",
                "notes": "VIP guest - arrange airport pickup"
            }
        }


class BookingResponseDTO(BaseModel):
    id: int
    request_id: int
    user_id: int
    vendor_id: Optional[int]
    vendor: Optional[dict] = None
    start_at: datetime
    end_at: Optional[datetime]
    start_at_formatted: Optional[str] = None
    end_at_formatted: Optional[str] = None
    status: str
    notes: Optional[str]
    created_at: datetime


class BookingListResponseDTO(BaseModel):
    bookings: List[BookingResponseDTO]
    total: int
    skip: int
    limit: int


class BookingStatusUpdateDTO(BaseModel):
    status: str  # upcoming, completed, cancelled
