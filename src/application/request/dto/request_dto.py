"""Request DTOs - API input/output schemas."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class RequestCreateDTO(BaseModel):
    """Input for creating a new request."""
    request_type: str = Field(..., description="Type: travel, dining, events, shopping")
    description: str = Field(..., min_length=10, description="Detailed request description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "request_type": "travel",
                "description": "I need a private jet from Riyadh to Dubai for 4 passengers next Friday."
            }
        }


class RequestResponseDTO(BaseModel):
    """Output for request responses."""
    id: int
    user_id: int
    request_type: str
    description: str
    status: str
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
