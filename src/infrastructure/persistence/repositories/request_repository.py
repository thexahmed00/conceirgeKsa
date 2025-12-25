"""Request repository implementation."""

from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.request.entities.request import Request
from src.infrastructure.persistence.models.request import RequestModel


class RequestRepository:
    """PostgreSQL implementation of request persistence."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, request: Request) -> Request:
        """Save a request and return with generated ID."""
        db_request = RequestModel(
            user_id=request.user_id,
            vendor_id=request.vendor_id,
            title=request.title,
            type=request.category_slug,
            description=request.description,
            status=request.status,
            created_at=request.created_at,
            updated_at=request.updated_at,
        )
        self.db.add(db_request)
        self.db.commit()
        self.db.refresh(db_request)
        
        return self._to_entity(db_request)
    
    def find_by_id(self, request_id: int) -> Optional[Request]:
        """Find request by ID."""
        db_request = self.db.query(RequestModel).filter(RequestModel.id == request_id).first()
        return self._to_entity(db_request) if db_request else None
    
    def find_by_user_id(self, user_id: int, skip: int = 0, limit: int = 20) -> List[Request]:
        """Find all requests for a user."""
        db_requests = (
            self.db.query(RequestModel)
            .filter(RequestModel.user_id == user_id)
            .order_by(RequestModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(r) for r in db_requests]
    
    def update(self, request: Request) -> Request:
        """Update an existing request."""
        db_request = self.db.query(RequestModel).filter(RequestModel.id == request.request_id).first()
        if db_request:
            db_request.status = request.status
            db_request.updated_at = request.updated_at
            self.db.commit()
            self.db.refresh(db_request)
            return self._to_entity(db_request)
        return request
    
    def _to_entity(self, model: RequestModel) -> Request:
        """Convert ORM model to domain entity."""
        return Request(
            request_id=model.id,
            user_id=model.user_id,
            title=model.title,
            category_slug=model.type,
            description=model.description,
            status=model.status,
            vendor_id=model.vendor_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
