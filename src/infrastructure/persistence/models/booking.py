"""SQLAlchemy Booking model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Index
from src.infrastructure.persistence.models.user import Base


class BookingModel(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("service_vendors.id"), nullable=True)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=False, default="upcoming")
    notes = Column(Text, nullable=True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_bookings_user_id', 'user_id'),
        Index('idx_bookings_status', 'status'),
        Index('idx_bookings_start_at', 'start_at'),
    )

    def __repr__(self) -> str:
        return f"<BookingModel(id={self.id}, request_id={self.request_id}, status={self.status})>"
