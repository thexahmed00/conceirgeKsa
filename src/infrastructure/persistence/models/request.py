"""SQLAlchemy Request model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.models.user import Base


class RequestModel(Base):
    """Request ORM model."""
    
    __tablename__ = "requests"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="new")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversation = relationship("ConversationModel", back_populates="request", uselist=False)
    
    __table_args__ = (
        Index('idx_requests_user_id', 'user_id'),
        Index('idx_requests_status', 'status'),
        Index('idx_requests_created_at', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<RequestModel(id={self.id}, type={self.type}, status={self.status})>"
