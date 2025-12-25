"""Request DTOs - API input/output schemas."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class RequestCreateDTO(BaseModel):
    """Input for creating a new request."""
    description: str = Field(..., min_length=10, description="Detailed request description")
    vendor_id: int = Field(..., description="Vendor ID - title and request type are derived from vendor")
    
    class Config:
        json_schema_extra = {
            "example": {
                "description": "I need a table for 4 at Cafe Bonjour this Friday at 8pm.",
                "vendor_id": 1
            }
        }


class RequestResponseDTO(BaseModel):
    """Output for request responses."""
    id: int
    user_id: int
    title: str
    category_slug: str
    description: str
    status: str
    vendor_id: Optional[int] = None
    vendor_name: Optional[str] = None
    conversation_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RequestListResponseDTO(BaseModel):
    """Paginated list of requests."""
    requests: List[RequestResponseDTO]
    total: int
    skip: int
    limit: int
