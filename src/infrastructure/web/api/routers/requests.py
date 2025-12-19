"""Request API endpoints."""

from fastapi import APIRouter, Depends, status, Query

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
from src.infrastructure.web.dependencies import (
    get_current_user,
    get_list_user_requests_use_case,
    get_request_use_case,
    get_submit_request_use_case,
)
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
    use_case: SubmitRequestUseCase = Depends(get_submit_request_use_case),
) -> RequestResponseDTO:
    """
    Submit a new concierge request.
    
    Creates a request + conversation + first message automatically.
    """
    result = use_case.execute(dto, user_id)
    logger.info(f"Request created: id={result.id}, user={user_id}")
    return result


@router.get("/", response_model=RequestListResponseDTO)
def list_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_id: int = Depends(get_current_user),
    use_case: ListUserRequestsUseCase = Depends(get_list_user_requests_use_case),
) -> RequestListResponseDTO:
    """List all requests for the current user."""
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
    use_case: GetRequestUseCase = Depends(get_request_use_case),
) -> RequestResponseDTO:
    """Get a specific request by ID."""
    return use_case.execute(request_id, user_id)
