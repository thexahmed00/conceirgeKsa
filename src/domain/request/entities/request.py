"""Request domain entity."""

from datetime import datetime
from typing import Optional
from src.domain.shared.exceptions import DomainException


class InvalidRequestError(DomainException):
    """Raised when request data is invalid."""
    pass


class Request:
    """Request aggregate - represents a concierge service request."""
    
    VALID_TYPES = ["travel", "dining", "events", "shopping"]
    VALID_STATUSES = ["new", "assigned", "in_progress", "fulfilled", "cancelled"]
    
    def __init__(
        self,
        request_id: Optional[int],
        user_id: int,
        request_type: str,
        description: str,
        status: str = "new",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.request_id = request_id
        self.user_id = user_id
        self.request_type = request_type
        self.description = description
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @classmethod
    def create(cls, user_id: int, request_type: str, description: str) -> "Request":
        """Factory method to create a new request with validation."""
        # Validate type
        if request_type not in cls.VALID_TYPES:
            raise InvalidRequestError(
                f"Invalid request type: {request_type}. Must be one of {cls.VALID_TYPES}"
            )
        
        # Validate description
        if not description or len(description.strip()) < 10:
            raise InvalidRequestError("Description must be at least 10 characters")
        
        return cls(
            request_id=None,
            user_id=user_id,
            request_type=request_type,
            description=description.strip(),
            status="new",
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
        return f"Request(id={self.request_id}, type={self.request_type}, status={self.status})"
