"""Request API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.application.request.dto.request_dto import (
    RequestCreateDTO,
    RequestResponseDTO,
    RequestListResponseDTO,
)
from src.application.request.use_cases.request_use_cases import (
    SubmitRequestUseCase,
    GetRequestUseCase,
    ListUserRequestsUseCase,
)
from src.infrastructure.persistence.repositories.request_repository import RequestRepository
from src.infrastructure.persistence.repositories.conversation_repository import ConversationRepository
from src.infrastructure.web.dependencies import get_db, get_current_user
from src.domain.request.entities.request import InvalidRequestError
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/requests",
    tags=["requests"],
)


@router.post("/", response_model=RequestResponseDTO, status_code=status.HTTP_201_CREATED)
def submit_request(
    dto: RequestCreateDTO,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RequestResponseDTO:
    """
    Submit a new concierge request.
    
    Creates a request + conversation + first message automatically.
    """
    try:
        request_repo = RequestRepository(db)
        conversation_repo = ConversationRepository(db)
        use_case = SubmitRequestUseCase(request_repo, conversation_repo)
        
        result = use_case.execute(dto, user_id)
        logger.info(f"Request created: id={result.id}, user={user_id}")
        
        return result
    
    except InvalidRequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating request: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create request")


@router.get("/", response_model=RequestListResponseDTO)
def list_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RequestListResponseDTO:
    """List all requests for the current user."""
    request_repo = RequestRepository(db)
    use_case = ListUserRequestsUseCase(request_repo)
    
    requests = use_case.execute(user_id, skip, limit)
    
    return RequestListResponseDTO(
        requests=requests,
        total=len(requests),
        skip=skip,
        limit=limit,
    )


@router.get("/{request_id}", response_model=RequestResponseDTO)
def get_request(
    request_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RequestResponseDTO:
    """Get a specific request by ID."""
    try:
        request_repo = RequestRepository(db)
        conversation_repo = ConversationRepository(db)
        use_case = GetRequestUseCase(request_repo, conversation_repo)
        
        return use_case.execute(request_id, user_id)
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
