"""Conversation DTOs - API input/output schemas."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class MessageCreateDTO(BaseModel):
    """Input for sending a message."""
    content: str = Field(..., min_length=1, description="Message content")
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "Could you also arrange airport transfers?"
            }
        }


class MessageResponseDTO(BaseModel):
    """Output for message responses."""
    id: int
    conversation_id: int
    sender_id: int
    sender_type: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationResponseDTO(BaseModel):
    """Output for conversation responses."""
    id: int
    request_id: int
    user_id: int
    created_at: datetime
    messages: List[MessageResponseDTO] = []
    
    class Config:
        from_attributes = True


class ConversationListResponseDTO(BaseModel):
    """Paginated list of conversations."""
    conversations: List[ConversationResponseDTO]
    total: int
    skip: int
    limit: int
