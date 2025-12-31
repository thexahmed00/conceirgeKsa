"""Booking use cases - application layer."""

from typing import List, Optional
from src.domain.booking.repository.booking_repository import BookingRepository
from src.domain.request.repository.request_repository import RequestRepository
from src.domain.service.repository.service_vendor_repository import ServiceVendorRepository
from src.domain.service.repository.vendor_image_repository import VendorImageRepository
from src.application.booking.dto.booking_dto import (
    BookingCreateDTO,
    BookingResponseDTO,
    BookingListResponseDTO,
)
from src.domain.booking.entities.booking import Booking
from src.domain.shared.exceptions import ResourceNotFoundError, AccessDeniedError, ValidationError


class CreateBookingUseCase:
    """Create a booking for a confirmed request (admin action)."""

    def __init__(self, booking_repo: BookingRepository, request_repo: RequestRepository):
        self.booking_repo = booking_repo
        self.request_repo = request_repo

    def execute(self, dto: BookingCreateDTO, admin_id: int) -> BookingResponseDTO:
        # Lookup request
        request = self.request_repo.find_by_id(dto.request_id)
        if not request:
            raise ResourceNotFoundError(f"Request {dto.request_id} not found")

        # Update request status to in_progress (admin confirmed)
        # Handle possible current statuses explicitly for clearer errors
        if request.status == "in_progress":
            # already in progress - nothing to do
            pass
        elif request.status == "assigned":
            request.start_progress()
        elif request.status == "new":
            # assign then start progress
            request.assign()
            request.start_progress()
        else:
            # cannot create booking for fulfilled/cancelled or unknown states
            raise ValidationError(f"Cannot confirm booking for request in status '{request.status}'")

        self.request_repo.update(request)

        # Create booking entity
        booking = Booking.create(
            request_id=dto.request_id,
            user_id=request.user_id,
            vendor_id=dto.vendor_id or request.vendor_id,
            start_at=dto.start_at,
            end_at=dto.end_at,
            created_by=admin_id,
            notes=dto.notes,
        )

        saved = self.booking_repo.save(booking)

        return BookingResponseDTO(
            id=saved.booking_id,
            request_id=saved.request_id,
            user_id=saved.user_id,
            vendor_id=saved.vendor_id,
            start_at=saved.start_at,
            end_at=saved.end_at,
            status=saved.status,
            notes=saved.notes,
            created_at=saved.created_at,
        )


class ListUserBookingsUseCase:
    def __init__(self, booking_repo: BookingRepository, vendor_repo: ServiceVendorRepository, image_repo: VendorImageRepository):
        self.booking_repo = booking_repo
        self.vendor_repo = vendor_repo
        self.image_repo = image_repo

    def _format_dt(self, dt):
        if not dt:
            return None
        try:
            return dt.strftime("%d %b %Y, %I:%M %p")
        except Exception:
            return None

    def execute(self, user_id: int, status: Optional[str] = None, skip: int = 0, limit: int = 20) -> BookingListResponseDTO:
        bookings = self.booking_repo.find_by_user_and_status(user_id, status, skip, limit)
        total = len(bookings)

        result_items = []
        for b in bookings:
            vendor_obj = None
            if b.vendor_id:
                v = self.vendor_repo.find_by_id(b.vendor_id)
                if v:
                    # try to get hero image URL from image repo (prefer direct hero image)
                    thumb = self.image_repo.find_first_hero_image(b.vendor_id)
                    hero_url = getattr(thumb, 'image_url', None) if thumb else None
                    vendor_obj = {"id": v.vendor_id, "name": v.name, "hero_url": hero_url}

            item = BookingResponseDTO(
                id=b.booking_id,
                request_id=b.request_id,
                user_id=b.user_id,
                vendor_id=b.vendor_id,
                vendor=vendor_obj,
                start_at=b.start_at,
                end_at=b.end_at,
                start_at_formatted=self._format_dt(b.start_at),
                end_at_formatted=self._format_dt(b.end_at),
                status=b.status,
                notes=b.notes,
                created_at=b.created_at,
            )
            result_items.append(item)

        return BookingListResponseDTO(
            bookings=result_items,
            total=total,
            skip=skip,
            limit=limit,
        )
