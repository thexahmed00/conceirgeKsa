"""User-facing bookings endpoints."""

from fastapi import APIRouter, Depends, Query
from typing import Optional

from src.application.booking.dto.booking_dto import BookingListResponseDTO
from src.infrastructure.web.dependencies import (
    get_list_user_bookings_use_case,
    get_current_user,
)

router = APIRouter(
    prefix="/api/v1",
    tags=["bookings"],
)


@router.get("/bookings", response_model=BookingListResponseDTO)
def list_user_bookings(
    status: Optional[str] = Query(None, description="Filter by status: upcoming|completed|cancelled"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_id: int = Depends(get_current_user),
    use_case = Depends(get_list_user_bookings_use_case),
) -> BookingListResponseDTO:
    return use_case.execute(user_id, status, skip, limit)
