"""Conversation API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.application.conversation.dto.conversation_dto import (
    MessageCreateDTO,
    MessageResponseDTO,
    ConversationResponseDTO,
    ConversationListResponseDTO,
)
from src.application.conversation.use_cases.conversation_use_cases import (
    GetConversationUseCase,
    SendMessageUseCase,
    ListUserConversationsUseCase,
)
from src.infrastructure.persistence.repositories.conversation_repository import ConversationRepository
from src.infrastructure.web.dependencies import get_db, get_current_user
from src.domain.conversation.entities.conversation import InvalidMessageError
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
    db: Session = Depends(get_db),
) -> ConversationListResponseDTO:
    """List all conversations for the current user."""
    conversation_repo = ConversationRepository(db)
    use_case = ListUserConversationsUseCase(conversation_repo)
    
    conversations = use_case.execute(user_id, skip, limit)
    
    return ConversationListResponseDTO(
        conversations=conversations,
        total=len(conversations),
        skip=skip,
        limit=limit,
    )


@router.get("/{conversation_id}", response_model=ConversationResponseDTO)
def get_conversation(
    conversation_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ConversationResponseDTO:
    """Get a conversation with all messages."""
    try:
        conversation_repo = ConversationRepository(db)
        use_case = GetConversationUseCase(conversation_repo)
        
        return use_case.execute(conversation_id, user_id)
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.post("/{conversation_id}/messages", response_model=MessageResponseDTO, status_code=status.HTTP_201_CREATED)
def send_message(
    conversation_id: int,
    dto: MessageCreateDTO,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageResponseDTO:
    """Send a message in a conversation."""
    try:
        conversation_repo = ConversationRepository(db)
        use_case = SendMessageUseCase(conversation_repo)
        
        result = use_case.execute(conversation_id, user_id, dto)
        logger.info(f"Message sent: conversation={conversation_id}, user={user_id}")
        
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except InvalidMessageError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
