"""SubscriptionRepository implementation - PostgreSQL persistence."""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from src.domain.plan.entities.subscription import Subscription, SubscriptionStatus
from src.domain.plan.repository.subscription_repository import SubscriptionRepository
from src.infrastructure.persistence.models.plan import SubscriptionModel


class PostgreSQLSubscriptionRepository(SubscriptionRepository):
    """SQLAlchemy-based SubscriptionRepository for PostgreSQL."""

    def __init__(self, db_session: Session):
        """Initialize repository with database session."""
        self._session = db_session

    def find_by_id(self, subscription_id: int) -> Optional[Subscription]:
        """Find a subscription by ID."""
        model = self._session.query(SubscriptionModel).filter(
            SubscriptionModel.id == subscription_id
        ).first()
        return self._to_entity(model) if model else None

    def find_by_user_id(self, user_id: int) -> List[Subscription]:
        """Find all subscriptions for a user."""
        models = self._session.query(SubscriptionModel).filter(
            SubscriptionModel.user_id == user_id
        ).order_by(SubscriptionModel.created_at.desc()).all()
        return [self._to_entity(model) for model in models]

    def find_active_by_user_id(self, user_id: int) -> Optional[Subscription]:
        """Find the active subscription for a user."""
        now = datetime.utcnow()
        model = self._session.query(SubscriptionModel).filter(
            SubscriptionModel.user_id == user_id,
            SubscriptionModel.status == SubscriptionStatus.ACTIVE,
            SubscriptionModel.start_date <= now,
            SubscriptionModel.end_date >= now
        ).first()
        return self._to_entity(model) if model else None

    def create(self, subscription: Subscription) -> Subscription:
        """Create a new subscription."""
        model = SubscriptionModel(
            user_id=subscription.user_id,
            plan_id=subscription.plan_id,
            status=subscription.status,
            start_date=subscription.start_date,
            end_date=subscription.end_date,
            payment_reference=subscription.payment_reference,
        )
        self._session.add(model)
        self._session.flush()
        subscription.subscription_id = model.id
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def update(self, subscription: Subscription) -> Subscription:
        """Update an existing subscription."""
        model = self._session.query(SubscriptionModel).filter(
            SubscriptionModel.id == subscription.subscription_id
        ).first()
        
        if model:
            model.status = subscription.status
            model.start_date = subscription.start_date
            model.end_date = subscription.end_date
            model.payment_reference = subscription.payment_reference
            self._session.commit()
            self._session.refresh(model)
            return self._to_entity(model)
        
        return subscription

    def find_by_payment_reference(self, payment_reference: str) -> Optional[Subscription]:
        """Find a subscription by payment reference."""
        model = self._session.query(SubscriptionModel).filter(
            SubscriptionModel.payment_reference == payment_reference
        ).first()
        return self._to_entity(model) if model else None

    def _to_entity(self, model: SubscriptionModel) -> Subscription:
        """Convert ORM model to domain entity."""
        return Subscription(
            subscription_id=model.id,
            user_id=model.user_id,
            plan_id=model.plan_id,
            status=model.status,
            start_date=model.start_date,
            end_date=model.end_date,
            payment_reference=model.payment_reference,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
