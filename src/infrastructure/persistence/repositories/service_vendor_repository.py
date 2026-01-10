"""ServiceVendor repository implementation."""

from typing import List, Optional, Tuple
from sqlalchemy.orm import Session, joinedload

from src.domain.service.entities.service_vendor import ServiceVendor
from src.domain.service.repository.service_vendor_repository import ServiceVendorRepository as IServiceVendorRepository
from src.infrastructure.persistence.models.service import ServiceVendorModel, ServiceCategoryModel


class ServiceVendorRepository(IServiceVendorRepository):
    """PostgreSQL implementation of ServiceVendor persistence."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, vendor: ServiceVendor) -> ServiceVendor:
        """Save a vendor and return with generated ID."""
        db_vendor = ServiceVendorModel(
            category_id=vendor.category_id,
            name=vendor.name,
            description=vendor.description,
            address=vendor.address,
            phone=vendor.phone,
            website=vendor.website,
            whatsapp=vendor.whatsapp,
            city=vendor.city,
            rating=vendor.rating,
            vendor_metadata=vendor.metadata,
            is_active=vendor.is_active,
            created_at=vendor.created_at,
            updated_at=vendor.updated_at,
        )
        self.db.add(db_vendor)
        self.db.commit()
        self.db.refresh(db_vendor)
        
        return self._to_entity(db_vendor)
    
    def find_by_id(self, vendor_id: int) -> Optional[ServiceVendor]:
        """Find vendor by ID."""
        db_vendor = (
            self.db.query(ServiceVendorModel)
            .options(joinedload(ServiceVendorModel.category))
            .filter(ServiceVendorModel.id == vendor_id)
            .first()
        )
        return self._to_entity(db_vendor) if db_vendor else None
    
    def find_by_category_id(
        self,
        category_id: int,
        skip: int = 0,
        limit: int = 20,
        active_only: bool = True,
        city: Optional[str] = None,
    ) -> Tuple[List[ServiceVendor], int]:
        """Find all vendors for a category with pagination and optional city filter."""
        query = (
            self.db.query(ServiceVendorModel)
            .options(joinedload(ServiceVendorModel.category))
            .filter(ServiceVendorModel.category_id == category_id)
        )
        
        if active_only:
            query = query.filter(ServiceVendorModel.is_active.is_(True))
        
        if city:
            query = query.filter(ServiceVendorModel.city == city)
        
        total = query.count()
        
        db_vendors = (
            query
            .order_by(ServiceVendorModel.rating.desc(), ServiceVendorModel.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        return [self._to_entity(v) for v in db_vendors], total
    
    def find_by_category_slug(
        self,
        category_slug: str,
        skip: int = 0,
        limit: int = 20,
        active_only: bool = True,
        city: Optional[str] = None,
    ) -> Tuple[List[ServiceVendor], int]:
        """Find all vendors for a category by slug with pagination and optional city filter."""
        query = (
            self.db.query(ServiceVendorModel)
            .join(ServiceCategoryModel)
            .options(joinedload(ServiceVendorModel.category))
            .filter(ServiceCategoryModel.slug == category_slug)
        )
        
        if active_only:
            query = query.filter(ServiceVendorModel.is_active.is_(True))
        
        if city:
            query = query.filter(ServiceVendorModel.city == city)
        
        total = query.count()
        
        db_vendors = (
            query
            .order_by(ServiceVendorModel.rating.desc(), ServiceVendorModel.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        return [self._to_entity(v) for v in db_vendors], total
    
    def find_all(
        self,
        skip: int = 0,
        limit: int = 20,
        active_only: bool = True,
        city: Optional[str] = None,
    ) -> Tuple[List[ServiceVendor], int]:
        """Find all vendors with pagination and optional city filter."""
        query = (
            self.db.query(ServiceVendorModel)
            .options(joinedload(ServiceVendorModel.category))
        )
        
        if active_only:
            query = query.filter(ServiceVendorModel.is_active.is_(True))
        
        if city:
            query = query.filter(ServiceVendorModel.city == city)
        
        total = query.count()
        
        db_vendors = (
            query
            .order_by(ServiceVendorModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        return [self._to_entity(v) for v in db_vendors], total
    
    def find_by_city(
        self,
        city: str,
        skip: int = 0,
        limit: int = 20,
        active_only: bool = True,
    ) -> Tuple[List[ServiceVendor], int]:
        """Find all vendors in a specific city with pagination."""
        query = (
            self.db.query(ServiceVendorModel)
            .options(joinedload(ServiceVendorModel.category))
            .filter(ServiceVendorModel.city == city)
        )
        
        if active_only:
            query = query.filter(ServiceVendorModel.is_active.is_(True))
        
        total = query.count()
        
        db_vendors = (
            query
            .order_by(ServiceVendorModel.rating.desc(), ServiceVendorModel.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        return [self._to_entity(v) for v in db_vendors], total
    
    def update(self, vendor: ServiceVendor) -> ServiceVendor:
        """Update an existing vendor."""
        db_vendor = (
            self.db.query(ServiceVendorModel)
            .filter(ServiceVendorModel.id == vendor.vendor_id)
            .first()
        )
        
        if db_vendor:
            db_vendor.name = vendor.name
            db_vendor.description = vendor.description
            db_vendor.address = vendor.address
            db_vendor.phone = vendor.phone
            db_vendor.website = vendor.website
            db_vendor.whatsapp = vendor.whatsapp
            db_vendor.city = vendor.city
            db_vendor.rating = vendor.rating
            db_vendor.vendor_metadata = vendor.metadata
            db_vendor.is_active = vendor.is_active
            db_vendor.updated_at = vendor.updated_at
            
            self.db.commit()
            self.db.refresh(db_vendor)
            return self._to_entity(db_vendor)
        
        return vendor
    
    def delete(self, vendor_id: int) -> bool:
        """Hard delete a vendor by ID."""
        db_vendor = (
            self.db.query(ServiceVendorModel)
            .filter(ServiceVendorModel.id == vendor_id)
            .first()
        )
        
        if db_vendor:
            self.db.delete(db_vendor)
            self.db.commit()
            return True
        
        return False
    
    def count_by_category(self, category_id: int, active_only: bool = True) -> int:
        """Count vendors in a category."""
        query = (
            self.db.query(ServiceVendorModel)
            .filter(ServiceVendorModel.category_id == category_id)
        )
        
        if active_only:
            query = query.filter(ServiceVendorModel.is_active.is_(True))
        
        return query.count()
    
    def _to_entity(self, model: ServiceVendorModel) -> ServiceVendor:
        """Convert ORM model to domain entity."""
        category_slug = None
        category_name = None
        
        if hasattr(model, 'category') and model.category:
            category_slug = model.category.slug
            category_name = model.category.name
        
        return ServiceVendor(
            vendor_id=model.id,
            category_id=model.category_id,
            name=model.name,
            description=model.description,
            address=model.address,
            phone=model.phone,
            website=model.website,
            whatsapp=model.whatsapp,
            city=model.city,
            rating=model.rating,
            metadata=model.vendor_metadata or {},
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
            category_slug=category_slug,
            category_name=category_name,
        )
