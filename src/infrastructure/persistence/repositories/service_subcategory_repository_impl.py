"""SQLAlchemy implementation of ServiceSubcategoryRepository."""

from typing import Optional, List
from sqlalchemy.orm import Session
from src.domain.service.repository.service_subcategory_repository import ServiceSubcategoryRepository
from src.domain.service.entities.service_subcategory import ServiceSubcategory
from src.infrastructure.persistence.models.service import ServiceSubcategoryModel


class ServiceSubcategoryRepositoryImpl(ServiceSubcategoryRepository):
    """SQLAlchemy-based ServiceSubcategoryRepository."""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def save(self, subcategory: ServiceSubcategory) -> ServiceSubcategory:
        """Save a new subcategory."""
        model = ServiceSubcategoryModel(
            category_id=subcategory.category_id,
            slug=subcategory.slug,
            name=subcategory.name,
            display_order=subcategory.display_order,
            icon_url=subcategory.icon_url,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        
        subcategory.subcategory_id = model.id
        return subcategory
    
    def find_by_id(self, subcategory_id: int) -> Optional[ServiceSubcategory]:
        """Find subcategory by ID."""
        model = self.db.query(ServiceSubcategoryModel).filter_by(id=subcategory_id).first()
        if not model:
            return None
        
        return ServiceSubcategory(
            subcategory_id=model.id,
            category_id=model.category_id,
            slug=model.slug,
            name=model.name,
            display_order=model.display_order,
            icon_url=model.icon_url,
            created_at=model.created_at,
        )
    
    def find_by_slug(self, slug: str) -> Optional[ServiceSubcategory]:
        """Find subcategory by slug."""
        model = self.db.query(ServiceSubcategoryModel).filter_by(slug=slug).first()
        if not model:
            return None
        
        return ServiceSubcategory(
            subcategory_id=model.id,
            category_id=model.category_id,
            slug=model.slug,
            name=model.name,
            display_order=model.display_order,
            icon_url=model.icon_url,
            created_at=model.created_at,
        )
    
    def find_by_category_id(self, category_id: int) -> List[ServiceSubcategory]:
        """Find all subcategories for a given category."""
        models = self.db.query(ServiceSubcategoryModel).filter_by(
            category_id=category_id
        ).order_by(ServiceSubcategoryModel.display_order).all()
        
        return [
            ServiceSubcategory(
                subcategory_id=m.id,
                category_id=m.category_id,
                slug=m.slug,
                name=m.name,
                display_order=m.display_order,
                icon_url=m.icon_url,
                created_at=m.created_at,
            )
            for m in models
        ]
    
    def find_all(self) -> List[ServiceSubcategory]:
        """Find all subcategories."""
        models = self.db.query(ServiceSubcategoryModel).order_by(
            ServiceSubcategoryModel.display_order
        ).all()
        
        return [
            ServiceSubcategory(
                subcategory_id=m.id,
                category_id=m.category_id,
                slug=m.slug,
                name=m.name,
                display_order=m.display_order,
                icon_url=m.icon_url,
                created_at=m.created_at,
            )
            for m in models
        ]
    
    def update(self, subcategory: ServiceSubcategory) -> ServiceSubcategory:
        """Update an existing subcategory."""
        model = self.db.query(ServiceSubcategoryModel).filter_by(
            id=subcategory.subcategory_id
        ).first()
        
        if not model:
            raise ValueError(f"Subcategory with id {subcategory.subcategory_id} not found")
        
        model.name = subcategory.name
        model.display_order = subcategory.display_order
        model.icon_url = subcategory.icon_url
        model.category_id = subcategory.category_id
        
        self.db.commit()
        self.db.refresh(model)
        
        return subcategory
    
    def delete(self, subcategory_id: int) -> bool:
        """Delete a subcategory by ID."""
        model = self.db.query(ServiceSubcategoryModel).filter_by(id=subcategory_id).first()
        
        if not model:
            return False
        
        self.db.delete(model)
        self.db.commit()
        return True
