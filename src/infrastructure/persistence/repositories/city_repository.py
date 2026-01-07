"""CityRepository implementation - PostgreSQL persistence."""

from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.content.entities.city import City
from src.domain.content.repository.city_repository import CityRepository
from src.infrastructure.persistence.models.content import CityModel


class PostgreSQLCityRepository(CityRepository):
    """SQLAlchemy-based CityRepository for PostgreSQL."""

    def __init__(self, db_session: Session):
        """Initialize repository with database session."""
        self._session = db_session

    async def find_all(self, active_only: bool = True) -> List[City]:
        """Find all cities."""
        query = self._session.query(CityModel)
        if active_only:
            query = query.filter(CityModel.is_active == True)
        
        models = query.order_by(CityModel.display_order.asc(), CityModel.name.asc()).all()
        return [self._to_entity(model) for model in models]

    async def find_by_id(self, city_id: int) -> Optional[City]:
        """Find a city by ID."""
        model = self._session.query(CityModel).filter(
            CityModel.id == city_id
        ).first()
        return self._to_entity(model) if model else None

    async def create(self, city: City) -> City:
        """Create a new city."""
        model = CityModel(
            name=city.name,
            name_ar=city.name_ar,
            country=city.country,
            display_order=city.display_order,
            is_active=city.is_active,
        )
        self._session.add(model)
        self._session.flush()
        city.city_id = model.id
        self._session.commit()
        return city

    async def update(self, city: City) -> City:
        """Update an existing city."""
        model = self._session.query(CityModel).filter(
            CityModel.id == city.city_id
        ).first()
        
        if model:
            model.name = city.name
            model.name_ar = city.name_ar
            model.country = city.country
            model.display_order = city.display_order
            model.is_active = city.is_active
            self._session.commit()
        
        return city

    async def delete(self, city_id: int) -> bool:
        """Delete a city by ID."""
        model = self._session.query(CityModel).filter(
            CityModel.id == city_id
        ).first()
        
        if model:
            self._session.delete(model)
            self._session.commit()
            return True
        return False

    def _to_entity(self, model: CityModel) -> City:
        """Convert ORM model to domain entity."""
        return City(
            city_id=model.id,
            name=model.name,
            name_ar=model.name_ar,
            country=model.country,
            display_order=model.display_order,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
