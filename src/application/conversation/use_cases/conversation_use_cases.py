"""Conversation use cases - application layer orchestration."""

from typing import List
from src.domain.conversation.entities.conversation import Message
from src.domain.conversation.repository.conversation_repository import ConversationRepository
from src.application.conversation.dto.conversation_dto import (
    MessageCreateDTO,
    MessageResponseDTO,
    ConversationResponseDTO,
    ConversationWithPaginatedMessagesDTO,
    ConversationListItemDTO,
)
from src.domain.shared.exceptions import AccessDeniedError, ResourceNotFoundError


class GetConversationUseCase:
    """Get a conversation with paginated messages."""
    
    def __init__(self, conversation_repo: ConversationRepository):
        self.conversation_repo = conversation_repo
    
    def execute(
        self,
        conversation_id: int,
        user_id: int,
        is_admin: bool = False,
        skip: int = 0,
        limit: int = 50,
    ) -> ConversationWithPaginatedMessagesDTO:
        conversation = self.conversation_repo.find_by_id(conversation_id)
        
        if not conversation:
            raise ResourceNotFoundError(f"Conversation {conversation_id} not found")
        
        # Check ownership (admins can access any conversation)
        if not is_admin and conversation.user_id != user_id:
            raise AccessDeniedError("You don't have access to this conversation")
        
        # Get paginated messages and total count in a single optimized call
        messages, total_messages = self.conversation_repo.get_messages_paginated(
            conversation_id, skip, limit
        )
        
        return ConversationWithPaginatedMessagesDTO(
            id=conversation.conversation_id,
            request_id=conversation.request_id,
            title=conversation.title,
            description=conversation.description,
            user_id=conversation.user_id,
            vendor_id=conversation.vendor_id,
            vendor_name=conversation.vendor_name,
            vendor_image_url=conversation.vendor_image_url,
            created_at=conversation.created_at,
            messages=[
                MessageResponseDTO(
                    id=m.message_id,
                    conversation_id=m.conversation_id,
                    sender_id=m.sender_id,
                    sender_type=m.sender_type,
                    content=m.content,
                    created_at=m.created_at,
                )
                for m in messages
            ],
            total_messages=total_messages,
            skip=skip,
            limit=limit,
        )


class SendMessageUseCase:
    """Send a message in a conversation."""
    
    def __init__(self, conversation_repo: ConversationRepository, notification_service=None):
        self.conversation_repo = conversation_repo
        self.notification_service = notification_service
    
    def execute(
        self,
        conversation_id: int,
        user_id: int,
        dto: MessageCreateDTO,
        sender_type: str = "user",
        sender_name: str = None,
    ) -> MessageResponseDTO:
        # Verify conversation exists and user has access
        conversation = self.conversation_repo.find_by_id(conversation_id)
        
        if not conversation:
            raise ResourceNotFoundError(f"Conversation {conversation_id} not found")
        
        # Check access (user or admin)
        if sender_type == "user" and conversation.user_id != user_id:
            raise AccessDeniedError("You don't have access to this conversation")
        
        # Create message
        message = Message.create(
            conversation_id=conversation_id,
            sender_id=user_id,
            sender_type=sender_type,
            content=dto.content,
        )
        
        # Save message
        saved_message = self.conversation_repo.add_message(message)
        
        # Send notification to the other party
        if self.notification_service:
            try:
                if sender_type == "admin":
                    # Admin sent message - notify the conversation's user
                    self.notification_service.notify_message_received(
                        user_id=conversation.user_id,
                        conversation_id=conversation_id,
                        sender_name=sender_name or "Support Team",
                    )
            except Exception:
                # Don't fail message sending if notification fails
                pass
        
        return MessageResponseDTO(
            id=saved_message.message_id,
            conversation_id=saved_message.conversation_id,
            sender_id=saved_message.sender_id,
            sender_type=saved_message.sender_type,
            content=saved_message.content,
            created_at=saved_message.created_at,
        )


class ListUserConversationsUseCase:
    """List all conversations for a user."""
    
    def __init__(self, conversation_repo: ConversationRepository):
        self.conversation_repo = conversation_repo
    
    def execute(self, user_id: int, skip: int = 0, limit: int = 20) -> List[ConversationListItemDTO]:
        conversations = self.conversation_repo.find_by_user_id(user_id, skip, limit)
        
        return [
            ConversationListItemDTO(
                id=c.conversation_id,
                request_id=c.request_id,
                vendor_id=c.vendor_id,
                vendor_name=c.vendor_name,
                vendor_image_url=c.vendor_image_url,
                category_slug=c.category_slug,
                last_message=c.messages[-1].content if c.messages else c.description,
                last_message_time=c.messages[-1].created_at if c.messages else c.created_at,
                unread_count=0,  # TODO: implement unread tracking
                created_at=c.created_at,
            )
            for c in conversations
        ]


class ListAllConversationsUseCase:
    """List all conversations (admin only)."""
    
    def __init__(self, conversation_repo: ConversationRepository):
        self.conversation_repo = conversation_repo
    
    def execute(self, skip: int = 0, limit: int = 20) -> tuple[List[ConversationResponseDTO], int]:
        conversations = self.conversation_repo.find_all(skip, limit)
        total = self.conversation_repo.count_all()
        
        return (
            [
                ConversationResponseDTO(
                    id=c.conversation_id,
                    request_id=c.request_id,
                    title=c.title,
                    description=c.description,
                    user_id=c.user_id,
                    created_at=c.created_at,
                    messages=[],  # Don't load messages for list view
                )
                for c in conversations
            ],
            total,
        )
