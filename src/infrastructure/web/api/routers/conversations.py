"""Conversation API endpoints."""

from fastapi import APIRouter, Depends, status, Query

from src.application.conversation.dto.conversation_dto import (
    MessageCreateDTO,
    MessageResponseDTO,
    ConversationResponseDTO,
    ConversationWithPaginatedMessagesDTO,
    ConversationListResponseDTO,
)
from src.application.conversation.use_cases.conversation_use_cases import (
    GetConversationUseCase,
    SendMessageUseCase,
    ListUserConversationsUseCase,
)
from src.infrastructure.web.dependencies import (
    get_conversation_use_case,
    get_current_user,
    get_list_user_conversations_use_case,
    get_send_message_use_case,
)
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/conversations",
    tags=["conversations"],
)


@router.get("/", response_model=ConversationListResponseDTO)
def list_conversations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_id: int = Depends(get_current_user),
    use_case: ListUserConversationsUseCase = Depends(get_list_user_conversations_use_case),
) -> ConversationListResponseDTO:
    """List all conversations for the current user."""
    conversations = use_case.execute(user_id, skip, limit)
    
    return ConversationListResponseDTO(
        conversations=conversations,
        total=len(conversations),
        skip=skip,
        limit=limit,
    )


@router.get("/{conversation_id}", response_model=ConversationWithPaginatedMessagesDTO)
def get_conversation(
    conversation_id: int,
    skip: int = Query(
        0,
        ge=0,
        description="Number of messages to skip when ordered by creation time (oldest first)",
    ),
    limit: int = Query(
        50,
        ge=1,
        le=100,
        description="Maximum number of messages to return after skipping, when ordered by creation time (oldest first)",
    ),
    user_id: int = Depends(get_current_user),
    use_case: GetConversationUseCase = Depends(get_conversation_use_case),
) -> ConversationWithPaginatedMessagesDTO:
    """Get a conversation with paginated messages."""
    return use_case.execute(conversation_id, user_id, skip=skip, limit=limit)


@router.post("/{conversation_id}/messages", response_model=MessageResponseDTO, status_code=status.HTTP_201_CREATED)
def send_message(
    conversation_id: int,
    dto: MessageCreateDTO,
    user_id: int = Depends(get_current_user),
    use_case: SendMessageUseCase = Depends(get_send_message_use_case),
) -> MessageResponseDTO:
    """Send a message in a conversation."""
    result = use_case.execute(conversation_id, user_id, dto)
    logger.info(f"Message sent: conversation={conversation_id}, user={user_id}")
    return result
