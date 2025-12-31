"""Booking repository implementation using SQLAlchemy."""

from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.booking.entities.booking import Booking
from src.infrastructure.persistence.models.booking import BookingModel


class BookingRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, booking: Booking) -> Booking:
        db_booking = BookingModel(
            request_id=booking.request_id,
            user_id=booking.user_id,
            vendor_id=booking.vendor_id,
            start_at=booking.start_at,
            end_at=booking.end_at,
            status=booking.status,
            notes=booking.notes,
            created_by=booking.created_by,
            created_at=booking.created_at,
        )
        self.db.add(db_booking)
        self.db.commit()
        self.db.refresh(db_booking)

        return self._to_entity(db_booking)

    def find_by_id(self, booking_id: int) -> Optional[Booking]:
        db_b = self.db.query(BookingModel).filter(BookingModel.id == booking_id).first()
        return self._to_entity(db_b) if db_b else None

    def find_by_user_and_status(self, user_id: int, status: Optional[str] = None, skip: int = 0, limit: int = 20) -> List[Booking]:
        q = self.db.query(BookingModel).filter(BookingModel.user_id == user_id)
        if status:
            q = q.filter(BookingModel.status == status)
        results = q.order_by(BookingModel.start_at.desc()).offset(skip).limit(limit).all()
        return [self._to_entity(b) for b in results]

    def update(self, booking: Booking) -> Booking:
        db_b = self.db.query(BookingModel).filter(BookingModel.id == booking.booking_id).first()
        if db_b:
            db_b.status = booking.status
            db_b.end_at = booking.end_at
            db_b.notes = booking.notes
            self.db.commit()
            self.db.refresh(db_b)
            return self._to_entity(db_b)
        return booking

    def _to_entity(self, model: BookingModel) -> Booking:
        return Booking(
            booking_id=model.id,
            request_id=model.request_id,
            user_id=model.user_id,
            vendor_id=model.vendor_id,
            start_at=model.start_at,
            end_at=model.end_at,
            status=model.status,
            notes=model.notes,
            created_at=model.created_at,
            created_by=model.created_by,
        )
