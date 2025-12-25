"""FastAPI dependency injection setup."""

from typing import Optional, Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.application.user.use_cases.user_use_cases import (
    AuthenticateUserUseCase,
    CreateUserUseCase,
    GetUserUseCase,
)
from src.application.request.use_cases.request_use_cases import (
    GetRequestUseCase,
    ListUserRequestsUseCase,
    SubmitRequestUseCase,
)
from src.application.conversation.use_cases.conversation_use_cases import (
    GetConversationUseCase,
    ListAllConversationsUseCase,
    ListUserConversationsUseCase,
    SendMessageUseCase,
)
from src.application.service.use_cases.service_category_use_cases import (
    ListCategoriesUseCase,
)
from src.application.service.use_cases.service_vendor_use_cases import (
    ListVendorsByCategoryUseCase,
    GetVendorDetailUseCase,
)
from src.application.service.use_cases.admin_vendor_use_cases import (
    CreateVendorUseCase,
    UpdateVendorUseCase,
    DeleteVendorUseCase,
)
from src.application.service.use_cases.vendor_image_use_cases import (
    AddVendorImageUseCase,
    DeleteVendorImageUseCase,
    ReorderVendorImagesUseCase,
    GetVendorImageUseCase,
)
from src.domain.request.repository.request_repository import RequestRepository
from src.domain.user.repository.user_repository import UserRepository
from src.infrastructure.persistence.database import SessionLocal
from src.infrastructure.persistence.repositories.conversation_repository import ConversationRepository
from src.infrastructure.persistence.repositories.request_repository import (
    RequestRepository as PostgreSQLRequestRepository,
)
from src.infrastructure.persistence.repositories.user_repository import PostgreSQLUserRepository
from src.infrastructure.persistence.repositories.service_category_repository import ServiceCategoryRepository
from src.infrastructure.persistence.repositories.service_vendor_repository import ServiceVendorRepository
from src.infrastructure.persistence.repositories.vendor_image_repository import VendorImageRepository
from src.infrastructure.auth.jwt_handler import get_user_id_from_token, get_token_claims
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides database session.
    
    Yields:
        SQLAlchemy Session instance
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """Provide a user repository bound to the current DB session."""
    return PostgreSQLUserRepository(db)


def get_create_user_use_case(
    user_repository: UserRepository = Depends(get_user_repository),
) -> CreateUserUseCase:
    return CreateUserUseCase(user_repository)


def get_authenticate_user_use_case(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(user_repository)


def get_user_use_case(
    user_repository: UserRepository = Depends(get_user_repository),
) -> GetUserUseCase:
    return GetUserUseCase(user_repository)


def get_request_repository(db: Session = Depends(get_db)) -> PostgreSQLRequestRepository:
    return PostgreSQLRequestRepository(db)


def get_conversation_repository(db: Session = Depends(get_db)) -> ConversationRepository:
    return ConversationRepository(db)


def get_service_vendor_repository(db: Session = Depends(get_db)) -> ServiceVendorRepository:
    """Provide a service vendor repository."""
    return ServiceVendorRepository(db)


def get_submit_request_use_case(
    request_repository: RequestRepository = Depends(get_request_repository),
    conversation_repository: ConversationRepository = Depends(get_conversation_repository),
    vendor_repository: ServiceVendorRepository = Depends(get_service_vendor_repository),
) -> SubmitRequestUseCase:
    return SubmitRequestUseCase(request_repository, conversation_repository, vendor_repository)


def get_request_use_case(
    request_repository: RequestRepository = Depends(get_request_repository),
    conversation_repository: ConversationRepository = Depends(get_conversation_repository),
) -> GetRequestUseCase:
    return GetRequestUseCase(request_repository, conversation_repository)


def get_list_user_requests_use_case(
    request_repository: RequestRepository = Depends(get_request_repository),
) -> ListUserRequestsUseCase:
    return ListUserRequestsUseCase(request_repository)


def get_conversation_use_case(
    conversation_repository: ConversationRepository = Depends(get_conversation_repository),
) -> GetConversationUseCase:
    return GetConversationUseCase(conversation_repository)


def get_send_message_use_case(
    conversation_repository: ConversationRepository = Depends(get_conversation_repository),
) -> SendMessageUseCase:
    return SendMessageUseCase(conversation_repository)


def get_list_user_conversations_use_case(
    conversation_repository: ConversationRepository = Depends(get_conversation_repository),
) -> ListUserConversationsUseCase:
    return ListUserConversationsUseCase(conversation_repository)


def get_list_all_conversations_use_case(
    conversation_repository: ConversationRepository = Depends(get_conversation_repository),
) -> ListAllConversationsUseCase:
    return ListAllConversationsUseCase(conversation_repository)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    """
    Dependency that validates JWT token and returns current user ID.
    
    Args:
        credentials: HTTP Bearer credentials with JWT token
        
    Returns:
        User ID from token claims
        
    Raises:
        HTTPException 401: If token invalid or expired
    """
    token = credentials.credentials
    
    user_id = get_user_id_from_token(token)
    if user_id is None:
        logger.warning("Invalid or expired token attempted")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_id


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[int]:
    """
    Optional user dependency - returns user ID if authenticated, None otherwise.
    
    Args:
        credentials: HTTP Bearer credentials (optional)
        
    Returns:
        User ID or None
    """
    if not credentials:
        return None
    
    return get_user_id_from_token(credentials.credentials)


# =============================================================================
# Service Domain Dependencies
# =============================================================================

def get_service_category_repository(db: Session = Depends(get_db)) -> ServiceCategoryRepository:
    """Provide a service category repository."""
    return ServiceCategoryRepository(db)


def get_vendor_image_repository(db: Session = Depends(get_db)) -> VendorImageRepository:
    """Provide a vendor image repository."""
    return VendorImageRepository(db)


def get_list_categories_use_case(
    category_repo: ServiceCategoryRepository = Depends(get_service_category_repository),
) -> ListCategoriesUseCase:
    """Provide use case for listing categories."""
    return ListCategoriesUseCase(category_repo)


def get_list_vendors_by_category_use_case(
    vendor_repo: ServiceVendorRepository = Depends(get_service_vendor_repository),
    image_repo: VendorImageRepository = Depends(get_vendor_image_repository),
) -> ListVendorsByCategoryUseCase:
    """Provide use case for listing vendors by category."""
    return ListVendorsByCategoryUseCase(vendor_repo, image_repo)


def get_vendor_detail_use_case(
    vendor_repo: ServiceVendorRepository = Depends(get_service_vendor_repository),
    image_repo: VendorImageRepository = Depends(get_vendor_image_repository),
) -> GetVendorDetailUseCase:
    """Provide use case for getting vendor details."""
    return GetVendorDetailUseCase(vendor_repo, image_repo)


def get_vendor_image_use_case(
    image_repo: VendorImageRepository = Depends(get_vendor_image_repository),
) -> GetVendorImageUseCase:
    """Provide use case for getting vendor images."""
    return GetVendorImageUseCase(image_repo)


def get_create_vendor_use_case(
    category_repo: ServiceCategoryRepository = Depends(get_service_category_repository),
    vendor_repo: ServiceVendorRepository = Depends(get_service_vendor_repository),
    image_repo: VendorImageRepository = Depends(get_vendor_image_repository),
) -> CreateVendorUseCase:
    """Provide use case for creating vendors (admin)."""
    return CreateVendorUseCase(category_repo, vendor_repo, image_repo)


def get_update_vendor_use_case(
    vendor_repo: ServiceVendorRepository = Depends(get_service_vendor_repository),
    image_repo: VendorImageRepository = Depends(get_vendor_image_repository),
) -> UpdateVendorUseCase:
    """Provide use case for updating vendors (admin)."""
    return UpdateVendorUseCase(vendor_repo, image_repo)


def get_delete_vendor_use_case(
    vendor_repo: ServiceVendorRepository = Depends(get_service_vendor_repository),
    image_repo: VendorImageRepository = Depends(get_vendor_image_repository),
) -> DeleteVendorUseCase:
    """Provide use case for deleting vendors (admin)."""
    return DeleteVendorUseCase(vendor_repo, image_repo)


def get_add_vendor_image_use_case(
    vendor_repo: ServiceVendorRepository = Depends(get_service_vendor_repository),
    image_repo: VendorImageRepository = Depends(get_vendor_image_repository),
) -> AddVendorImageUseCase:
    """Provide use case for adding vendor images (admin)."""
    return AddVendorImageUseCase(vendor_repo, image_repo)


def get_delete_vendor_image_use_case(
    vendor_repo: ServiceVendorRepository = Depends(get_service_vendor_repository),
    image_repo: VendorImageRepository = Depends(get_vendor_image_repository),
) -> DeleteVendorImageUseCase:
    """Provide use case for deleting vendor images (admin)."""
    return DeleteVendorImageUseCase(vendor_repo, image_repo)


def get_reorder_vendor_images_use_case(
    vendor_repo: ServiceVendorRepository = Depends(get_service_vendor_repository),
    image_repo: VendorImageRepository = Depends(get_vendor_image_repository),
) -> ReorderVendorImagesUseCase:
    """Provide use case for reordering vendor images (admin)."""
    return ReorderVendorImagesUseCase(vendor_repo, image_repo)


def get_current_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    """
    Dependency that validates JWT token and checks if user is admin.
    Uses cached is_admin claim from JWT to avoid database query.
    
    Returns:
        Admin user ID
        
    Raises:
        HTTPException 401: If token invalid
        HTTPException 403: If user is not admin
    """
    token = credentials.credentials
    
    # Get all claims including is_admin from JWT (no DB query)
    claims = get_token_claims(token)
    if not claims or not claims.get("user_id"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check admin status from cached JWT claim
    if not claims.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    
    return claims["user_id"]
