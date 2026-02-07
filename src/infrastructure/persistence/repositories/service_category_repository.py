"""ServiceCategory repository implementation."""

from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.service.entities.service_category import ServiceCategory
from src.domain.service.entities.service_subcategory import ServiceSubcategory
from src.domain.service.repository.service_category_repository import ServiceCategoryRepository as IServiceCategoryRepository
from src.infrastructure.persistence.models.service import ServiceCategoryModel, ServiceSubcategoryModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload


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
            icon_url=getattr(category, 'icon_url', None),
            created_at=category.created_at,
        )
        self.db.add(db_category)
        try:
            self.db.commit()
            self.db.refresh(db_category)
            return self._to_entity(db_category)
        except IntegrityError:
            # Unique constraint on slug violated — translate to a clear error
            self.db.rollback()
            raise ValueError(f"Category with slug '{category.slug}' already exists")
    
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
    
    def find_all_with_subcategories(self) -> List[dict]:
        """Find all categories with their subcategories eagerly loaded."""
        db_categories = (
            self.db.query(ServiceCategoryModel)
            .options(joinedload(ServiceCategoryModel.subcategories))
            .order_by(ServiceCategoryModel.display_order.asc())
            .all()
        )
        result = []
        for cat in db_categories:
            category_entity = self._to_entity(cat)
            subcategory_entities = [
                ServiceSubcategory(
                    subcategory_id=sc.id,
                    category_id=sc.category_id,
                    slug=sc.slug,
                    name=sc.name,
                    display_order=sc.display_order,
                    icon_url=sc.icon_url,
                    created_at=sc.created_at,
                )
                for sc in sorted(cat.subcategories, key=lambda s: s.display_order)
            ]
            result.append({
                "category": category_entity,
                "subcategories": subcategory_entities,
            })
        return result
    
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
            db_category.icon_url = getattr(category, 'icon_url', None)
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
            icon_url=getattr(model, 'icon_url', None),
            created_at=model.created_at,
        )
