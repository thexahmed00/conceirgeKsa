"""Conversation and Message domain entities."""

from datetime import datetime
from typing import Optional, List
from src.domain.shared.exceptions import DomainException


class InvalidMessageError(DomainException):
    """Raised when message data is invalid."""
    pass


class Message:
    """Message value object - belongs to a Conversation."""
    
    VALID_SENDER_TYPES = ["user", "admin"]
    
    def __init__(
        self,
        message_id: Optional[int],
        conversation_id: int,
        sender_id: int,
        sender_type: str,
        content: str,
        created_at: Optional[datetime] = None,
    ):
        self.message_id = message_id
        self.conversation_id = conversation_id
        self.sender_id = sender_id
        self.sender_type = sender_type
        self.content = content
        self.created_at = created_at or datetime.utcnow()
    
    @classmethod
    def create(
        cls,
        conversation_id: int,
        sender_id: int,
        sender_type: str,
        content: str,
    ) -> "Message":
        """Create a new message with validation."""
        if sender_type not in cls.VALID_SENDER_TYPES:
            raise InvalidMessageError(f"Invalid sender type: {sender_type}")
        
        if not content or len(content.strip()) == 0:
            raise InvalidMessageError("Message content cannot be empty")
        
        return cls(
            message_id=None,
            conversation_id=conversation_id,
            sender_id=sender_id,
            sender_type=sender_type,
            content=content.strip(),
        )
    
    def __repr__(self) -> str:
        return f"Message(id={self.message_id}, sender={self.sender_type})"


class Conversation:
    """Conversation aggregate - chat thread linked to a request."""
    
    def __init__(
        self,
        conversation_id: Optional[int],
        request_id: int,
        user_id: int,
        created_at: Optional[datetime] = None,
        messages: Optional[List[Message]] = None,
    ):
        self.conversation_id = conversation_id
        self.request_id = request_id
        self.user_id = user_id
        self.created_at = created_at or datetime.utcnow()
        self.messages = messages or []
    
    @classmethod
    def create(cls, request_id: int, user_id: int) -> "Conversation":
        """Create a new conversation."""
        return cls(
            conversation_id=None,
            request_id=request_id,
            user_id=user_id,
        )
    
    def add_message(self, sender_id: int, sender_type: str, content: str) -> Message:
        """Add a message to this conversation."""
        if self.conversation_id is None:
            raise InvalidMessageError("Cannot add message to unsaved conversation")
        
        message = Message.create(
            conversation_id=self.conversation_id,
            sender_id=sender_id,
            sender_type=sender_type,
            content=content,
        )
        self.messages.append(message)
        return message
    
    def __repr__(self) -> str:
        return f"Conversation(id={self.conversation_id}, request_id={self.request_id})"
