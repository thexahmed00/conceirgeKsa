"""Admin API endpoints for concierge agents."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel

from src.application.conversation.dto.conversation_dto import (
    MessageCreateDTO,
    MessageResponseDTO,
    ConversationResponseDTO,
    AdminConversationListResponseDTO,
)
from src.application.booking.dto.booking_dto import BookingCreateDTO, BookingResponseDTO
from src.application.conversation.use_cases.conversation_use_cases import (
    GetConversationUseCase,
    SendMessageUseCase,
    ListAllConversationsUseCase,
)
from src.domain.user.repository.user_repository import UserRepository
from src.infrastructure.web.dependencies import (
    get_conversation_use_case,
    get_current_user,
    get_send_message_use_case,
    get_user_repository,
    get_create_booking_use_case,
    get_current_admin_user,
    get_list_all_conversations_use_case,
)
from src.infrastructure.web.dependencies import get_conversation_repository
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


@router.get("/conversations", response_model=AdminConversationListResponseDTO)
def list_all_conversations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    admin_id: int = Depends(get_admin_user),
    use_case: ListAllConversationsUseCase = Depends(get_list_all_conversations_use_case),
) -> AdminConversationListResponseDTO:
    """Admin-only: list conversations across all users."""
    conversations, total = use_case.execute(skip=skip, limit=limit)
    logger.info(f"Admin {admin_id} listed conversations: skip={skip} limit={limit} total={total}")
    return AdminConversationListResponseDTO(
        conversations=conversations,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationResponseDTO)
def get_conversation_by_id(
    conversation_id: int,
    admin_id: int = Depends(get_admin_user),
    use_case: GetConversationUseCase = Depends(get_conversation_use_case),
) -> ConversationResponseDTO:
    """Admin-only: get any conversation (with messages) by id."""
    return use_case.execute(conversation_id=conversation_id, user_id=admin_id, is_admin=True)





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


@router.post("/conversations/{conversation_id}/confirm", response_model=BookingResponseDTO, status_code=201)
def confirm_conversation_and_create_booking(
    conversation_id: int,
    dto: BookingCreateDTO,
    admin_id: int = Depends(get_admin_user),
    conversation_repo = Depends(get_conversation_repository),
    create_booking_uc = Depends(get_create_booking_use_case),
) -> BookingResponseDTO:
    """Admin confirms a conversation (linked to a request) and creates a booking for the user.

    The client only needs to provide the `conversation_id` in the path and the booking times in the body.
    The server will resolve the linked `request_id` and `user_id` from the conversation.
    """
    conversation = conversation_repo.find_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Populate missing request_id/vendor_id from conversation
    if not dto.request_id:
        dto.request_id = conversation.request_id
    if not dto.vendor_id:
        dto.vendor_id = conversation.vendor_id

    # Execute booking creation
    result = create_booking_uc.execute(dto, admin_id)
    logger.info(f"Admin {admin_id} created booking {result.id} for conversation {conversation_id} (request {dto.request_id})")
    return result
