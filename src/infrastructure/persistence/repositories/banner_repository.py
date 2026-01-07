"""BannerRepository implementation - PostgreSQL persistence."""

from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.content.entities.banner import Banner
from src.domain.content.repository.banner_repository import BannerRepository
from src.infrastructure.persistence.models.content import BannerModel


class PostgreSQLBannerRepository(BannerRepository):
    """SQLAlchemy-based BannerRepository for PostgreSQL."""

    def __init__(self, db_session: Session):
        """Initialize repository with database session."""
        self._session = db_session

    async def find_all(self, active_only: bool = True) -> List[Banner]:
        """Find all banners."""
        query = self._session.query(BannerModel)
        if active_only:
            query = query.filter(BannerModel.is_active == True)
        
        models = query.order_by(BannerModel.display_order.asc()).all()
        return [self._to_entity(model) for model in models]

    async def find_by_id(self, banner_id: int) -> Optional[Banner]:
        """Find a banner by ID."""
        model = self._session.query(BannerModel).filter(
            BannerModel.id == banner_id
        ).first()
        return self._to_entity(model) if model else None

    async def create(self, banner: Banner) -> Banner:
        """Create a new banner."""
        model = BannerModel(
            title=banner.title,
            image_url=banner.image_url,
            description=banner.description,
            link_url=banner.link_url,
            display_order=banner.display_order,
            is_active=banner.is_active,
        )
        self._session.add(model)
        self._session.flush()
        banner.banner_id = model.id
        self._session.commit()
        return banner

    async def update(self, banner: Banner) -> Banner:
        """Update an existing banner."""
        model = self._session.query(BannerModel).filter(
            BannerModel.id == banner.banner_id
        ).first()
        
        if model:
            model.title = banner.title
            model.image_url = banner.image_url
            model.description = banner.description
            model.link_url = banner.link_url
            model.display_order = banner.display_order
            model.is_active = banner.is_active
            self._session.commit()
        
        return banner

    async def delete(self, banner_id: int) -> bool:
        """Delete a banner by ID."""
        model = self._session.query(BannerModel).filter(
            BannerModel.id == banner_id
        ).first()
        
        if model:
            self._session.delete(model)
            self._session.commit()
            return True
        return False

    def _to_entity(self, model: BannerModel) -> Banner:
        """Convert ORM model to domain entity."""
        return Banner(
            banner_id=model.id,
            title=model.title,
            image_url=model.image_url,
            description=model.description,
            link_url=model.link_url,
            display_order=model.display_order,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
