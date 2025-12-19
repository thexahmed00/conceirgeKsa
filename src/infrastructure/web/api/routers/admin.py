"""Admin API endpoints for concierge agents."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel

from src.application.conversation.dto.conversation_dto import (
    MessageCreateDTO,
    MessageResponseDTO,
    ConversationResponseDTO,
    ConversationListResponseDTO,
)
from src.application.conversation.use_cases.conversation_use_cases import (
    GetConversationUseCase,
    SendMessageUseCase,
    ListAllConversationsUseCase,
)
from src.domain.user.repository.user_repository import UserRepository
from src.infrastructure.web.dependencies import (
    get_conversation_use_case,
    get_current_user,
    get_list_all_conversations_use_case,
    get_send_message_use_case,
    get_user_repository,
)
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["admin"],
)


class AdminInfo(BaseModel):
    """Admin user info response."""
    user_id: int
    is_admin: bool


async def get_admin_user(
    user_id: int = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repository),
):
    """Dependency to ensure user is an admin."""
    user = await user_repo.find_by_id(user_id)
    
    if not user or not getattr(user, 'is_admin', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return user_id


@router.get("/me", response_model=AdminInfo)
async def get_admin_info(
    admin_id: int = Depends(get_admin_user),
) -> AdminInfo:
    """Get current admin info."""
    return AdminInfo(user_id=admin_id, is_admin=True)


@router.get("/conversations", response_model=ConversationListResponseDTO)
def list_all_conversations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    admin_id: int = Depends(get_admin_user),
    use_case: ListAllConversationsUseCase = Depends(get_list_all_conversations_use_case),
) -> ConversationListResponseDTO:
    """List all conversations (admin only)."""
    conversations, total = use_case.execute(skip, limit)
    
    logger.info(f"Admin {admin_id} listed all conversations: {total} total")
    
    return ConversationListResponseDTO(
        conversations=conversations,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationResponseDTO)
def get_conversation(
    conversation_id: int,
    admin_id: int = Depends(get_admin_user),
    use_case: GetConversationUseCase = Depends(get_conversation_use_case),
) -> ConversationResponseDTO:
    """Get a conversation with all messages (admin access)."""
    return use_case.execute(conversation_id, admin_id, is_admin=True)


@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponseDTO, status_code=status.HTTP_201_CREATED)
def send_admin_message(
    conversation_id: int,
    dto: MessageCreateDTO,
    admin_id: int = Depends(get_admin_user),
    use_case: SendMessageUseCase = Depends(get_send_message_use_case),
) -> MessageResponseDTO:
    """Send a message as admin in any conversation."""
    result = use_case.execute(conversation_id, admin_id, dto, sender_type="admin")
    logger.info(f"Admin {admin_id} sent message in conversation {conversation_id}")
    return result
