"""Admin API endpoints for concierge agents."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

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
from src.infrastructure.persistence.repositories.conversation_repository import ConversationRepository
from src.infrastructure.web.dependencies import get_db, get_current_user
from src.domain.conversation.entities.conversation import InvalidMessageError
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


async def get_admin_user(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Dependency to ensure user is an admin."""
    from src.infrastructure.persistence.repositories.user_repository import PostgreSQLUserRepository
    
    user_repo = PostgreSQLUserRepository(db)
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
    db: Session = Depends(get_db),
) -> ConversationListResponseDTO:
    """List all conversations (admin only)."""
    conversation_repo = ConversationRepository(db)
    use_case = ListAllConversationsUseCase(conversation_repo)
    
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
    db: Session = Depends(get_db),
) -> ConversationResponseDTO:
    """Get a conversation with all messages (admin access)."""
    try:
        conversation_repo = ConversationRepository(db)
        use_case = GetConversationUseCase(conversation_repo)
        
        # Admin can access any conversation
        return use_case.execute(conversation_id, admin_id, is_admin=True)
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponseDTO, status_code=status.HTTP_201_CREATED)
def send_admin_message(
    conversation_id: int,
    dto: MessageCreateDTO,
    admin_id: int = Depends(get_admin_user),
    db: Session = Depends(get_db),
) -> MessageResponseDTO:
    """Send a message as admin in any conversation."""
    try:
        conversation_repo = ConversationRepository(db)
        use_case = SendMessageUseCase(conversation_repo)
        
        # Send message as admin
        result = use_case.execute(conversation_id, admin_id, dto, sender_type="admin")
        logger.info(f"Admin {admin_id} sent message in conversation {conversation_id}")
        
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidMessageError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
