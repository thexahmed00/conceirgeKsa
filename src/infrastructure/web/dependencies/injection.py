"""FastAPI dependency injection setup."""

from typing import Optional, Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.application.user.use_cases.user_use_cases import (
    AuthenticateUserUseCase,
    CreateUserUseCase,
    GetUserUseCase,
    ListAllUsersUseCase,
    GetUserByIdUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
    CreateAdminUserUseCase,
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
    ListCategoriesWithSubcategoriesUseCase,
    CreateCategoryUseCase,
    UpdateCategoryUseCase,
)
from src.application.service.use_cases.service_subcategory_use_cases import (
    CreateSubcategoryUseCase,
    UpdateSubcategoryUseCase,
    GetSubcategoryUseCase,
    ListSubcategoriesByCategoryUseCase,
    ListAllSubcategoriesUseCase,
    DeleteSubcategoryUseCase,
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
from src.application.booking.use_cases.booking_use_cases import (
    CreateBookingUseCase,
    ListAllBookingsUseCase,
    ListUserBookingsUseCase,
    UpdateBookingStatusUseCase,
)
from src.application.plan.use_cases.plan_use_cases import (
    ListPlansUseCase,
    PurchasePlanUseCase,
    VerifyPaymentUseCase,
    GetUserSubscriptionUseCase,
)
from src.application.content.use_cases.content_use_cases import (
    ListBannersUseCase,
    ListCitiesUseCase,
    CreateBannerUseCase,
    UpdateBannerUseCase,
    DeleteBannerUseCase,
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
from src.infrastructure.persistence.repositories.service_subcategory_repository_impl import ServiceSubcategoryRepositoryImpl
from src.infrastructure.persistence.repositories.service_vendor_repository import ServiceVendorRepository
from src.infrastructure.persistence.repositories.vendor_image_repository import VendorImageRepository
from src.infrastructure.persistence.repositories.booking_repository import BookingRepository
from src.infrastructure.persistence.repositories.plan.plan_repository import PostgreSQLPlanRepository
from src.infrastructure.persistence.repositories.plan.subscription_repository import PostgreSQLSubscriptionRepository
from src.infrastructure.persistence.repositories.notification_repository import PostgreSQLNotificationRepository
from src.infrastructure.persistence.repositories.banner_repository import PostgreSQLBannerRepository
from src.infrastructure.persistence.repositories.city_repository import PostgreSQLCityRepository
from src.infrastructure.auth.jwt_handler import get_user_id_from_token, get_token_claims
from src.shared.logger.config import get_logger
from src.application.notification.services.notification_service import NotificationService

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


def get_list_all_users_use_case(
    user_repository: UserRepository = Depends(get_user_repository),
) -> ListAllUsersUseCase:
    """Provide use case for listing all users (admin)."""
    return ListAllUsersUseCase(user_repository)


def get_user_by_id_use_case(
    user_repository: UserRepository = Depends(get_user_repository),
) -> GetUserByIdUseCase:
    """Provide use case for getting a specific user by ID (admin)."""
    return GetUserByIdUseCase(user_repository)


def get_update_user_use_case(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UpdateUserUseCase:
    """Provide use case for updating a user (admin)."""
    return UpdateUserUseCase(user_repository)


def get_delete_user_use_case(
    user_repository: UserRepository = Depends(get_user_repository),
) -> DeleteUserUseCase:
    """Provide use case for deleting a user (admin)."""
    return DeleteUserUseCase(user_repository)


def get_create_admin_user_use_case(
    user_repository: UserRepository = Depends(get_user_repository),
) -> CreateAdminUserUseCase:
    """Provide use case for creating a user with optional admin privileges (admin)."""
    return CreateAdminUserUseCase(user_repository)


def get_request_repository(db: Session = Depends(get_db)) -> PostgreSQLRequestRepository:
    return PostgreSQLRequestRepository(db)


def get_conversation_repository(db: Session = Depends(get_db)) -> ConversationRepository:
    return ConversationRepository(db)


def get_service_vendor_repository(db: Session = Depends(get_db)) -> ServiceVendorRepository:
    """Provide a service vendor repository."""
    return ServiceVendorRepository(db)


def get_booking_repository(db: Session = Depends(get_db)) -> BookingRepository:
    """Provide booking repository."""
    return BookingRepository(db)


def get_vendor_image_repository(db: Session = Depends(get_db)) -> VendorImageRepository:
    """Provide a vendor image repository (moved earlier to avoid forward-reference issues)."""
    return VendorImageRepository(db)


def get_submit_request_use_case(
    request_repository: RequestRepository = Depends(get_request_repository),
    conversation_repository: ConversationRepository = Depends(get_conversation_repository),
    vendor_repository: ServiceVendorRepository = Depends(get_service_vendor_repository),
    user_repository: UserRepository = Depends(get_user_repository),
    db: Session = Depends(get_db),
) -> SubmitRequestUseCase:
    notification_service = NotificationService(db)
    return SubmitRequestUseCase(
        request_repository,
        conversation_repository,
        vendor_repository,
        notification_service,
        user_repository,
    )


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
    db: Session = Depends(get_db),
) -> SendMessageUseCase:
    notification_service = NotificationService(db)
    return SendMessageUseCase(conversation_repository, notification_service)


def get_list_user_conversations_use_case(
    conversation_repository: ConversationRepository = Depends(get_conversation_repository),
) -> ListUserConversationsUseCase:
    return ListUserConversationsUseCase(conversation_repository)


def get_create_booking_use_case(
    booking_repo: BookingRepository = Depends(get_booking_repository),
    request_repo: RequestRepository = Depends(get_request_repository),
    vendor_repo: ServiceVendorRepository = Depends(get_service_vendor_repository),
    db: Session = Depends(get_db),
) -> CreateBookingUseCase:
    notification_service = NotificationService(db)
    return CreateBookingUseCase(booking_repo, request_repo, vendor_repo, notification_service)


def get_list_user_bookings_use_case(
    booking_repo: BookingRepository = Depends(get_booking_repository),
    vendor_repo: ServiceVendorRepository = Depends(get_service_vendor_repository),
    image_repo: VendorImageRepository = Depends(get_vendor_image_repository),
) -> ListUserBookingsUseCase:
    return ListUserBookingsUseCase(booking_repo, vendor_repo, image_repo)


def get_list_all_bookings_use_case(
    booking_repo: BookingRepository = Depends(get_booking_repository),
    vendor_repo: ServiceVendorRepository = Depends(get_service_vendor_repository),
    image_repo: VendorImageRepository = Depends(get_vendor_image_repository),
) -> ListAllBookingsUseCase:
    return ListAllBookingsUseCase(booking_repo, vendor_repo, image_repo)


def get_booking_detail_use_case(
    booking_repo: BookingRepository = Depends(get_booking_repository),
    request_repo: PostgreSQLRequestRepository = Depends(get_request_repository),
    vendor_repo: ServiceVendorRepository = Depends(get_service_vendor_repository),
    image_repo: VendorImageRepository = Depends(get_vendor_image_repository),
    user_repo: UserRepository = Depends(get_user_repository),
    conversation_repo: ConversationRepository = Depends(get_conversation_repository),
) -> "GetBookingDetailUseCase":
    from src.application.booking.use_cases.booking_use_cases import GetBookingDetailUseCase
    return GetBookingDetailUseCase(
        booking_repo, request_repo, vendor_repo, image_repo, user_repo, conversation_repo
    )


def get_update_booking_status_use_case(
    booking_repo: BookingRepository = Depends(get_booking_repository),
    db: Session = Depends(get_db),
) -> UpdateBookingStatusUseCase:
    notification_service = NotificationService(db)
    return UpdateBookingStatusUseCase(booking_repo, notification_service)


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


def get_list_categories_with_subcategories_use_case(
    category_repo: ServiceCategoryRepository = Depends(get_service_category_repository),
) -> ListCategoriesWithSubcategoriesUseCase:
    """Provide use case for listing categories with nested subcategories."""
    return ListCategoriesWithSubcategoriesUseCase(category_repo)


def get_create_category_use_case(
    category_repo: ServiceCategoryRepository = Depends(get_service_category_repository),
    subcategory_repo = Depends(get_service_subcategory_repository),
) -> CreateCategoryUseCase:
    """Provide use case for creating a category (admin)."""
    return CreateCategoryUseCase(category_repo, subcategory_repo)




def get_update_category_use_case(
    category_repo: ServiceCategoryRepository = Depends(get_service_category_repository),
) -> UpdateCategoryUseCase:
    """Provide use case for updating a category (admin)."""
    return UpdateCategoryUseCase(category_repo)


# =============================================================================
# Service Subcategory Dependencies
# =============================================================================

def get_service_subcategory_repository(db: Session = Depends(get_db)):
    """Provide a service subcategory repository."""
    return ServiceSubcategoryRepositoryImpl(db)


def get_create_subcategory_use_case(
    subcategory_repo = Depends(get_service_subcategory_repository),
    category_repo: ServiceCategoryRepository = Depends(get_service_category_repository),
) -> CreateSubcategoryUseCase:
    """Provide use case for creating a subcategory (admin)."""
    return CreateSubcategoryUseCase(subcategory_repo, category_repo)


def get_update_subcategory_use_case(
    subcategory_repo = Depends(get_service_subcategory_repository),
    category_repo: ServiceCategoryRepository = Depends(get_service_category_repository),
) -> UpdateSubcategoryUseCase:
    """Provide use case for updating a subcategory (admin)."""
    return UpdateSubcategoryUseCase(subcategory_repo, category_repo)


def get_get_subcategory_use_case(
    subcategory_repo = Depends(get_service_subcategory_repository),
) -> GetSubcategoryUseCase:
    """Provide use case for getting a subcategory."""
    return GetSubcategoryUseCase(subcategory_repo)


def get_list_subcategories_by_category_use_case(
    subcategory_repo = Depends(get_service_subcategory_repository),
) -> ListSubcategoriesByCategoryUseCase:
    """Provide use case for listing subcategories by category."""
    return ListSubcategoriesByCategoryUseCase(subcategory_repo)


def get_list_all_subcategories_use_case(
    subcategory_repo = Depends(get_service_subcategory_repository),
) -> ListAllSubcategoriesUseCase:
    """Provide use case for listing all subcategories."""
    return ListAllSubcategoriesUseCase(subcategory_repo)


def get_delete_subcategory_use_case(
    subcategory_repo = Depends(get_service_subcategory_repository),
) -> DeleteSubcategoryUseCase:
    """Provide use case for deleting a subcategory (admin)."""
    return DeleteSubcategoryUseCase(subcategory_repo)


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
    
    return claims.get("user_id")


# ============= Plan Dependencies =============

def get_plan_repository(db: Session = Depends(get_db)) -> PostgreSQLPlanRepository:
    """Provide a plan repository."""
    return PostgreSQLPlanRepository(db)


def get_subscription_repository(db: Session = Depends(get_db)) -> PostgreSQLSubscriptionRepository:
    """Provide a subscription repository."""
    return PostgreSQLSubscriptionRepository(db)


def get_list_plans_use_case(
    plan_repo: PostgreSQLPlanRepository = Depends(get_plan_repository),
) -> ListPlansUseCase:
    """Provide list plans use case."""
    return ListPlansUseCase(plan_repo)


def get_purchase_plan_use_case(
    plan_repo: PostgreSQLPlanRepository = Depends(get_plan_repository),
    subscription_repo: PostgreSQLSubscriptionRepository = Depends(get_subscription_repository),
    user_repo: UserRepository = Depends(get_user_repository),
) -> PurchasePlanUseCase:
    """Provide purchase plan use case."""
    return PurchasePlanUseCase(plan_repo, subscription_repo, user_repo)


def get_verify_payment_use_case(
    subscription_repo: PostgreSQLSubscriptionRepository = Depends(get_subscription_repository),
    user_repo: UserRepository = Depends(get_user_repository),
    plan_repo: PostgreSQLPlanRepository = Depends(get_plan_repository),
    db: Session = Depends(get_db),
) -> VerifyPaymentUseCase:
    """Provide verify payment use case."""
    notification_service = NotificationService(db)
    return VerifyPaymentUseCase(subscription_repo, user_repo, plan_repo, notification_service)


def get_user_subscription_use_case(
    subscription_repo: PostgreSQLSubscriptionRepository = Depends(get_subscription_repository),
    plan_repo: PostgreSQLPlanRepository = Depends(get_plan_repository),
) -> GetUserSubscriptionUseCase:
    """Provide get user subscription use case."""
    return GetUserSubscriptionUseCase(subscription_repo, plan_repo)


# Content/Banner dependencies
def get_banner_repository(db: Session = Depends(get_db)) -> PostgreSQLBannerRepository:
    """Provide a banner repository."""
    return PostgreSQLBannerRepository(db)


def get_city_repository(db: Session = Depends(get_db)) -> PostgreSQLCityRepository:
    """Provide a city repository."""
    return PostgreSQLCityRepository(db)


def get_list_banners_use_case(
    banner_repo: PostgreSQLBannerRepository = Depends(get_banner_repository),
) -> ListBannersUseCase:
    """Provide list banners use case."""
    return ListBannersUseCase(banner_repo)


def get_list_cities_use_case(
    city_repo: PostgreSQLCityRepository = Depends(get_city_repository),
) -> ListCitiesUseCase:
    """Provide list cities use case."""
    return ListCitiesUseCase(city_repo)


def get_create_banner_use_case(
    banner_repo: PostgreSQLBannerRepository = Depends(get_banner_repository),
) -> CreateBannerUseCase:
    """Provide create banner use case."""
    return CreateBannerUseCase(banner_repo)


def get_update_banner_use_case(
    banner_repo: PostgreSQLBannerRepository = Depends(get_banner_repository),
) -> UpdateBannerUseCase:
    """Provide update banner use case."""
    return UpdateBannerUseCase(banner_repo)


def get_delete_banner_use_case(
    banner_repo: PostgreSQLBannerRepository = Depends(get_banner_repository),
) -> DeleteBannerUseCase:
    """Provide delete banner use case."""
    return DeleteBannerUseCase(banner_repo)
