"""ServiceCategory repository implementation."""

from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.service.entities.service_category import ServiceCategory
from src.domain.service.repository.service_category_repository import ServiceCategoryRepository as IServiceCategoryRepository
from src.infrastructure.persistence.models.service import ServiceCategoryModel


class ServiceCategoryRepository(IServiceCategoryRepository):
    """PostgreSQL implementation of ServiceCategory persistence."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, category: ServiceCategory) -> ServiceCategory:
        """Save a category and return with generated ID."""
        db_category = ServiceCategoryModel(
            slug=category.slug,
            name=category.name,
            display_order=category.display_order,
            created_at=category.created_at,
        )
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        
        return self._to_entity(db_category)
    
    def find_by_id(self, category_id: int) -> Optional[ServiceCategory]:
        """Find category by ID."""
        db_category = (
            self.db.query(ServiceCategoryModel)
            .filter(ServiceCategoryModel.id == category_id)
            .first()
        )
        return self._to_entity(db_category) if db_category else None
    
    def find_by_slug(self, slug: str) -> Optional[ServiceCategory]:
        """Find category by slug."""
        db_category = (
            self.db.query(ServiceCategoryModel)
            .filter(ServiceCategoryModel.slug == slug)
            .first()
        )
        return self._to_entity(db_category) if db_category else None
    
    def find_all(self) -> List[ServiceCategory]:
        """Find all categories ordered by display_order."""
        db_categories = (
            self.db.query(ServiceCategoryModel)
            .order_by(ServiceCategoryModel.display_order.asc())
            .all()
        )
        return [self._to_entity(c) for c in db_categories]
    
    def update(self, category: ServiceCategory) -> ServiceCategory:
        """Update an existing category."""
        db_category = (
            self.db.query(ServiceCategoryModel)
            .filter(ServiceCategoryModel.id == category.category_id)
            .first()
        )
        
        if db_category:
            db_category.name = category.name
            db_category.display_order = category.display_order
            self.db.commit()
            self.db.refresh(db_category)
            return self._to_entity(db_category)
        
        return category
    
    def delete(self, category_id: int) -> bool:
        """Delete a category by ID."""
        db_category = (
            self.db.query(ServiceCategoryModel)
            .filter(ServiceCategoryModel.id == category_id)
            .first()
        )
        
        if db_category:
            self.db.delete(db_category)
            self.db.commit()
            return True
        
        return False
    
    def _to_entity(self, model: ServiceCategoryModel) -> ServiceCategory:
        """Convert ORM model to domain entity."""
        return ServiceCategory(
            category_id=model.id,
            slug=model.slug,
            name=model.name,
            display_order=model.display_order,
            created_at=model.created_at,
        )
