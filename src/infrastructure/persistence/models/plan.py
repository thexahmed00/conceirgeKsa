"""SQLAlchemy Plan and Subscription models."""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Float,
    ForeignKey, Index, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.models.user import Base
from src.domain.plan.entities.subscription import SubscriptionStatus


class PlanModel(Base):
    """SQLAlchemy model for subscription plans."""
    
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    duration_days = Column(Integer, nullable=False)  # 30, 365, etc.
    tier = Column(Integer, nullable=False)  # 5000, 10000, 15000, etc.
    features = Column(Text, nullable=True)  # JSON string of features
    is_active = Column(Boolean, nullable=False, default=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subscriptions = relationship("SubscriptionModel", back_populates="plan")
    
    __table_args__ = (
        Index('idx_plan_active', 'is_active'),
        Index('idx_plan_tier', 'tier'),
    )
    
    def __repr__(self) -> str:
        return f"<PlanModel(id={self.id}, name={self.name}, tier={self.tier})>"


class SubscriptionModel(Base):
    """SQLAlchemy model for user subscriptions."""
    
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    
    status = Column(
        SQLEnum(SubscriptionStatus, name='subscription_status'),
        nullable=False,
        default=SubscriptionStatus.PENDING
    )
    
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    payment_reference = Column(String(255), nullable=True, unique=True, index=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    plan = relationship("PlanModel", back_populates="subscriptions")
    
    __table_args__ = (
        Index('idx_subscription_user', 'user_id'),
        Index('idx_subscription_status', 'status'),
        Index('idx_subscription_payment_ref', 'payment_reference'),
    )
    
    def __repr__(self) -> str:
        return f"<SubscriptionModel(id={self.id}, user_id={self.user_id}, status={self.status})>"
