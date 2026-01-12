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


class ConversationListItemDTO(BaseModel):
    """Output for conversation list item (minimal info for list view)."""
    id: int
    request_id: int
    vendor_id: Optional[int] = None
    vendor_name: Optional[str] = None
    vendor_image_url: Optional[str] = None
    category_slug: Optional[str] = None
    last_message: Optional[str] = None
    last_message_time: Optional[datetime] = None
    unread_count: int = 0  # Future: implement unread tracking
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationResponseDTO(BaseModel):
    """Output for conversation responses (full detail)."""
    id: int
    request_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    user_id: int
    vendor_id: Optional[int] = None
    vendor_name: Optional[str] = None
    vendor_image_url: Optional[str] = None
    created_at: datetime
    messages: List[MessageResponseDTO] = []
    
    class Config:
        from_attributes = True


class ConversationWithPaginatedMessagesDTO(BaseModel):
    """Output for conversation with paginated messages."""
    id: int
    request_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    user_id: int
    vendor_id: Optional[int] = None
    vendor_name: Optional[str] = None
    vendor_image_url: Optional[str] = None
    created_at: datetime
    messages: List[MessageResponseDTO] = []
    total_messages: int
    skip: int
    limit: int
    
    class Config:
        from_attributes = True


class ConversationListResponseDTO(BaseModel):
    """Paginated list of conversations."""
    conversations: List[ConversationListItemDTO]
    total: int
    skip: int
    limit: int


class AdminConversationListResponseDTO(BaseModel):
    """Paginated list of conversations for admin inbox views."""
    conversations: List[ConversationResponseDTO]
    total: int
    skip: int
    limit: int
