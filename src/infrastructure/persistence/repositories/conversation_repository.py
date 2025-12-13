"""Conversation repository implementation."""

from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.conversation.entities.conversation import Conversation, Message
from src.infrastructure.persistence.models.conversation import ConversationModel, MessageModel


class ConversationRepository:
    """PostgreSQL implementation of conversation persistence."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, conversation: Conversation) -> Conversation:
        """Save a conversation and return with generated ID."""
        db_conversation = ConversationModel(
            request_id=conversation.request_id,
            user_id=conversation.user_id,
            created_at=conversation.created_at,
        )
        self.db.add(db_conversation)
        self.db.commit()
        self.db.refresh(db_conversation)
        
        return self._to_entity(db_conversation)
    
    def find_by_id(self, conversation_id: int) -> Optional[Conversation]:
        """Find conversation by ID with messages."""
        db_conversation = (
            self.db.query(ConversationModel)
            .filter(ConversationModel.id == conversation_id)
            .first()
        )
        if not db_conversation:
            return None
        
        # Load messages
        db_messages = (
            self.db.query(MessageModel)
            .filter(MessageModel.conversation_id == conversation_id)
            .order_by(MessageModel.created_at.asc())
            .all()
        )
        
        return self._to_entity(db_conversation, db_messages)
    
    def find_by_request_id(self, request_id: int) -> Optional[Conversation]:
        """Find conversation by request ID."""
        db_conversation = (
            self.db.query(ConversationModel)
            .filter(ConversationModel.request_id == request_id)
            .first()
        )
        if not db_conversation:
            return None
        
        db_messages = (
            self.db.query(MessageModel)
            .filter(MessageModel.conversation_id == db_conversation.id)
            .order_by(MessageModel.created_at.asc())
            .all()
        )
        
        return self._to_entity(db_conversation, db_messages)
    
    def find_by_user_id(self, user_id: int, skip: int = 0, limit: int = 20) -> List[Conversation]:
        """Find all conversations for a user."""
        db_conversations = (
            self.db.query(ConversationModel)
            .filter(ConversationModel.user_id == user_id)
            .order_by(ConversationModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(c) for c in db_conversations]
    
    def find_all(self, skip: int = 0, limit: int = 20) -> List[Conversation]:
        """Find all conversations (admin use)."""
        db_conversations = (
            self.db.query(ConversationModel)
            .order_by(ConversationModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(c) for c in db_conversations]
    
    def count_all(self) -> int:
        """Count all conversations."""
        return self.db.query(ConversationModel).count()
    
    def add_message(self, message: Message) -> Message:
        """Add a message to a conversation."""
        db_message = MessageModel(
            conversation_id=message.conversation_id,
            sender_id=message.sender_id,
            sender_type=message.sender_type,
            content=message.content,
            created_at=message.created_at,
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        
        return self._message_to_entity(db_message)
    
    def get_messages(
        self, conversation_id: int, skip: int = 0, limit: int = 50
    ) -> List[Message]:
        """Get messages for a conversation with pagination."""
        db_messages = (
            self.db.query(MessageModel)
            .filter(MessageModel.conversation_id == conversation_id)
            .order_by(MessageModel.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._message_to_entity(m) for m in db_messages]
    
    def _to_entity(
        self, model: ConversationModel, messages: List[MessageModel] = None
    ) -> Conversation:
        """Convert ORM model to domain entity."""
        return Conversation(
            conversation_id=model.id,
            request_id=model.request_id,
            user_id=model.user_id,
            created_at=model.created_at,
            messages=[self._message_to_entity(m) for m in (messages or [])],
        )
    
    def _message_to_entity(self, model: MessageModel) -> Message:
        """Convert message ORM model to domain entity."""
        return Message(
            message_id=model.id,
            conversation_id=model.conversation_id,
            sender_id=model.sender_id,
            sender_type=model.sender_type,
            content=model.content,
            created_at=model.created_at,
        )
