"""Conversation repository implementation."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload, selectinload

from src.domain.conversation.entities.conversation import Conversation, Message
from src.infrastructure.persistence.models.conversation import ConversationModel, MessageModel
from src.infrastructure.persistence.models.request import RequestModel
from src.infrastructure.persistence.models.service import ServiceVendorModel, VendorImageModel


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
            .options(joinedload(ConversationModel.messages))
            .options(joinedload(ConversationModel.request))
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
        """Find all conversations for a user with eager loading."""
        db_conversations = (
            self.db.query(ConversationModel)
            .join(RequestModel, ConversationModel.request_id == RequestModel.id)
            .options(
                joinedload(ConversationModel.request)
                .joinedload(RequestModel.vendor)
                .joinedload(ServiceVendorModel.category)
            )
            .options(
                joinedload(ConversationModel.request)
                .joinedload(RequestModel.vendor)
                .selectinload(ServiceVendorModel.images)
            )
            .options(selectinload(ConversationModel.messages))
            .filter(ConversationModel.user_id == user_id)
            .order_by(ConversationModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(c) for c in db_conversations]
    
    def find_all(self, skip: int = 0, limit: int = 20) -> List[Conversation]:
        """Find all conversations (admin use) with eager loading."""
        db_conversations = (
            self.db.query(ConversationModel)
            .options(
                joinedload(ConversationModel.request)
                .joinedload(RequestModel.vendor)
                .joinedload(ServiceVendorModel.category)
            )
            .options(
                joinedload(ConversationModel.request)
                .joinedload(RequestModel.vendor)
                .selectinload(ServiceVendorModel.images)
            )
            .options(joinedload(ConversationModel.user))
            .options(selectinload(ConversationModel.messages))
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
        """Convert ORM model to domain entity using eagerly loaded relationships."""
        # Extract title and description from the related request
        title = None
        description = None
        vendor_id = None
        vendor_name = None
        vendor_image_url = None
        category_slug = None
        
        if hasattr(model, 'request') and model.request:
            title = model.request.title
            description = model.request.description
            vendor_id = model.request.vendor_id
            
            # Use eagerly loaded vendor info (no additional queries)
            vendor = getattr(model.request, 'vendor', None)
            if vendor:
                vendor_name = vendor.name
                category = getattr(vendor, 'category', None)
                if category:
                    category_slug = category.slug
                # Get first hero image from eagerly loaded images
                images = getattr(vendor, 'images', []) or []
                hero_images = sorted(
                    [img for img in images if img.image_type == "hero"],
                    key=lambda x: x.display_order
                )
                if hero_images:
                    vendor_image_url = hero_images[0].image_url
        
        # Use provided messages or load from model
        message_entities = []
        if messages is not None:
            message_entities = [self._message_to_entity(m) for m in messages]
        elif hasattr(model, 'messages') and model.messages:
            message_entities = [self._message_to_entity(m) for m in model.messages]
        
        return Conversation(
            conversation_id=model.id,
            request_id=model.request_id,
            user_id=model.user_id,
            title=title,
            description=description,
            vendor_id=vendor_id,
            vendor_name=vendor_name,
            vendor_image_url=vendor_image_url,
            category_slug=category_slug,
            created_at=model.created_at,
            messages=message_entities,
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
