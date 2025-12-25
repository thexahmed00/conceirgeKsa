"""Request domain entity."""

from datetime import datetime
from typing import Optional
from src.domain.shared.exceptions import DomainException


class InvalidRequestError(DomainException):
    """Raised when request data is invalid."""
    pass


class Request:
    """Request aggregate - represents a concierge service request."""
    
    VALID_STATUSES = ["new", "assigned", "in_progress", "fulfilled", "cancelled"]
    
    def __init__(
        self,
        request_id: Optional[int],
        user_id: int,
        title: str,
        category_slug: str,
        description: str,
        status: str = "new",
        vendor_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.request_id = request_id
        self.user_id = user_id
        self.title = title
        self.category_slug = category_slug
        self.description = description
        self.status = status
        self.vendor_id = vendor_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @classmethod
    def create(
        cls,
        user_id: int,
        title: str,
        category_slug: str,
        description: str,
        vendor_id: Optional[int] = None,
    ) -> "Request":
        """Factory method to create a new request with validation."""
        # Validate description
        if not description or len(description.strip()) < 10:
            raise InvalidRequestError("Description must be at least 10 characters")
        
        return cls(
            request_id=None,
            user_id=user_id,
            title=title.strip(),
            category_slug=category_slug,
            description=description.strip(),
            status="new",
            vendor_id=vendor_id,
        )
    
    def assign(self) -> None:
        """Mark request as assigned to a concierge."""
        if self.status != "new":
            raise InvalidRequestError("Can only assign new requests")
        self.status = "assigned"
        self.updated_at = datetime.utcnow()
    
    def start_progress(self) -> None:
        """Mark request as in progress."""
        if self.status != "assigned":
            raise InvalidRequestError("Can only start progress on assigned requests")
        self.status = "in_progress"
        self.updated_at = datetime.utcnow()
    
    def fulfill(self) -> None:
        """Mark request as fulfilled."""
        if self.status != "in_progress":
            raise InvalidRequestError("Can only fulfill requests in progress")
        self.status = "fulfilled"
        self.updated_at = datetime.utcnow()
    
    def cancel(self) -> None:
        """Cancel the request."""
        if self.status in ["fulfilled", "cancelled"]:
            raise InvalidRequestError("Cannot cancel fulfilled or already cancelled requests")
        self.status = "cancelled"
        self.updated_at = datetime.utcnow()
    
    def __repr__(self) -> str:
        return f"Request(id={self.request_id}, category={self.category_slug}, status={self.status})"
