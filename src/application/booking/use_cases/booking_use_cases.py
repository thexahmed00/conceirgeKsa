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
from src.shared.logger.config import get_logger

logger = get_logger(__name__)


class CreateBookingUseCase:
    """Create a booking for a confirmed request (admin action)."""

    def __init__(self, booking_repo: BookingRepository, request_repo: RequestRepository, vendor_repo: ServiceVendorRepository = None, notification_service=None):
        self.booking_repo = booking_repo
        self.request_repo = request_repo
        self.vendor_repo = vendor_repo
        self.notification_service = notification_service

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
        
        # Notify user about request status update
        if self.notification_service:
            try:
                self.notification_service.notify_request_updated(
                    user_id=request.user_id,
                    request_id=request.request_id,
                    status=request.status,
                )
            except Exception as e:
                # Don't fail booking creation if notification fails
                logger.error(f"Failed to send request update notification: {e}")

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

        # Send notification to user about booking confirmation
        if self.notification_service and self.vendor_repo:
            try:
                vendor = self.vendor_repo.find_by_id(saved.vendor_id)
                booking_details = f"{vendor.name}" if vendor else "your booking"
                self.notification_service.notify_booking_confirmed(
                    user_id=saved.user_id,
                    booking_id=saved.booking_id,
                    booking_details=booking_details,
                )
            except Exception as e:
                # Don't fail booking creation if notification fails
                logger.error(f"Failed to send booking notification: {e}")

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
        normalized_status = status.lower().strip() if status else None
        if normalized_status and normalized_status not in Booking.VALID_STATUSES:
            raise ValidationError(
                "Invalid status. Expected one of: upcoming|completed|cancelled"
            )

        total = self.booking_repo.count_by_user_and_status(user_id, normalized_status)
        bookings = self.booking_repo.find_by_user_and_status(user_id, normalized_status, skip, limit)

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


class ListAllBookingsUseCase:
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

    def execute(self, status: Optional[str] = None, skip: int = 0, limit: int = 20) -> BookingListResponseDTO:
        normalized_status = status.lower().strip() if status else None
        if normalized_status and normalized_status not in Booking.VALID_STATUSES:
            raise ValidationError(
                "Invalid status. Expected one of: upcoming|completed|cancelled"
            )

        total = self.booking_repo.count_all(normalized_status)
        bookings = self.booking_repo.find_all(normalized_status, skip, limit)

        result_items = []
        for b in bookings:
            vendor_obj = None
            if b.vendor_id:
                v = self.vendor_repo.find_by_id(b.vendor_id)
                if v:
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


class UpdateBookingStatusUseCase:
    """Admin use case to update booking status."""

    def __init__(self, booking_repo: BookingRepository, notification_service=None):
        self.booking_repo = booking_repo
        self.notification_service = notification_service

    def execute(self, booking_id: int, new_status: str, admin_id: int) -> BookingResponseDTO:
        # Validate status
        normalized_status = new_status.lower().strip()
        if normalized_status not in Booking.VALID_STATUSES:
            raise ValidationError(
                f"Invalid status '{new_status}'. Expected one of: upcoming|completed|cancelled"
            )

        # Find booking
        booking = self.booking_repo.find_by_id(booking_id)
        if not booking:
            raise ResourceNotFoundError(f"Booking {booking_id} not found")

        old_status = booking.status

        # Update status based on action
        if normalized_status == "completed":
            booking.complete()
        elif normalized_status == "cancelled":
            booking.cancel()
        elif normalized_status == "upcoming":
            # Allow resetting to upcoming if not completed
            if booking.status == "completed":
                raise ValidationError("Cannot change completed booking back to upcoming")
            booking.status = "upcoming"

        # Save changes
        updated_booking = self.booking_repo.update(booking)

        # Notify user about status change
        if self.notification_service and old_status != normalized_status:
            try:
                if normalized_status == "completed":
                    from src.domain.notification.entities.notification import NotificationType
                    self.notification_service.create_notification(
                        user_id=updated_booking.user_id,
                        title="Booking Completed",
                        message="Your booking has been completed successfully. Thank you for choosing our services! We hope you had a great experience.",
                        notification_type=NotificationType.GENERAL,
                        related_id=booking_id,
                    )
                elif normalized_status == "cancelled":
                    self.notification_service.notify_booking_cancelled(
                        user_id=updated_booking.user_id,
                        booking_id=booking_id,
                    )
            except Exception as e:
                logger.error(f"Failed to send booking status notification: {e}")

        logger.info(f"Admin {admin_id} updated booking {booking_id} status from {old_status} to {normalized_status}")

        return BookingResponseDTO(
            id=updated_booking.booking_id,
            request_id=updated_booking.request_id,
            user_id=updated_booking.user_id,
            vendor_id=updated_booking.vendor_id,
            start_at=updated_booking.start_at,
            end_at=updated_booking.end_at,
            status=updated_booking.status,
            notes=updated_booking.notes,
            created_at=updated_booking.created_at,
        )
