"""PlanRepository implementation - PostgreSQL persistence."""

from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.plan.entities.plan import Plan
from src.domain.plan.repository.plan_repository import PlanRepository
from src.infrastructure.persistence.models.plan import PlanModel


class PostgreSQLPlanRepository(PlanRepository):
    """SQLAlchemy-based PlanRepository for PostgreSQL."""

    def __init__(self, db_session: Session):
        """Initialize repository with database session."""
        self._session = db_session

    def find_all(self, active_only: bool = True) -> List[Plan]:
        """Find all plans."""
        query = self._session.query(PlanModel)
        if active_only:
            query = query.filter(PlanModel.is_active == True)
        
        models = query.order_by(PlanModel.tier.asc()).all()
        return [self._to_entity(model) for model in models]

    def find_by_id(self, plan_id: int) -> Optional[Plan]:
        """Find a plan by ID."""
        model = self._session.query(PlanModel).filter(
            PlanModel.id == plan_id
        ).first()
        return self._to_entity(model) if model else None

    def create(self, plan: Plan) -> Plan:
        """Create a new plan."""
        model = PlanModel(
            name=plan.name,
            description=plan.description,
            price=plan.price,
            duration_days=plan.duration_days,
            tier=plan.tier,
            features=plan.features,
            is_active=plan.is_active,
        )
        self._session.add(model)
        self._session.flush()
        plan.plan_id = model.id
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def update(self, plan: Plan) -> Plan:
        """Update an existing plan."""
        model = self._session.query(PlanModel).filter(
            PlanModel.id == plan.plan_id
        ).first()
        
        if model:
            model.name = plan.name
            model.description = plan.description
            model.price = plan.price
            model.duration_days = plan.duration_days
            model.tier = plan.tier
            model.features = plan.features
            model.is_active = plan.is_active
            self._session.commit()
            self._session.refresh(model)
            return self._to_entity(model)
        
        return plan

    def delete(self, plan_id: int) -> bool:
        """Delete a plan by ID."""
        model = self._session.query(PlanModel).filter(
            PlanModel.id == plan_id
        ).first()
        
        if model:
            self._session.delete(model)
            self._session.commit()
            return True
        return False

    def _to_entity(self, model: PlanModel) -> Plan:
        """Convert ORM model to domain entity."""
        return Plan(
            plan_id=model.id,
            name=model.name,
            description=model.description,
            price=model.price,
            duration_days=model.duration_days,
            tier=model.tier,
            features=model.features,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
