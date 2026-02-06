"""SQLAlchemy User model - Database ORM representation."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Index, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from src.domain.plan.entities.plan_tier import PlanTier

Base = declarative_base()


class UserModel(Base):
    """SQLAlchemy User model for database persistence."""
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Core fields
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    full_name = Column(String(256), nullable=False)
    phone_number = Column(String(20), nullable=True)
    tier = Column(
        SQLEnum(
            PlanTier,
            name='plan_tier',
            values_callable=lambda enum: [e.value for e in enum],
            create_type=False,  # Don't create type, already exists from plans table
        ),
        nullable=True,
        default=PlanTier.LIFESTYLE,
    )
    is_active = Column(Boolean, nullable=False, default=True)
    is_admin = Column(Boolean, nullable=False, default=False)  # Admin flag
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversations = relationship("ConversationModel", back_populates="user")
    
    # Indexes for query performance
    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_created', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<UserModel(id={self.id}, email={self.email})>"
