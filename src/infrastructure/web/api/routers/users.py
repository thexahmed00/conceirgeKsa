"""User Profile API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.user.dto.user_dto import UserResponse, UserUpdateRequest
from src.domain.user.repository.user_repository import UserRepository
from src.infrastructure.web.dependencies import get_current_user, get_user_repository
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    user_id: int = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserResponse:
    """Get the current authenticated user's profile."""
    user = await user_repo.find_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=user.user_id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        full_name=f"{user.first_name} {user.last_name}",
        phone_number=user.phone_number,
        tier=getattr(user, 'tier', 5000),
        is_active=getattr(user, 'is_active', True),
        created_at=user.created_at,
        is_admin=getattr(user, 'is_admin', False),
        updated_at=user.updated_at,
    )


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    update_data: UserUpdateRequest,
    user_id: int = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserResponse:
    """Update the current authenticated user's profile."""
    user = await user_repo.find_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields if provided
    if update_data.first_name is not None:
        user.first_name = update_data.first_name
    if update_data.last_name is not None:
        user.last_name = update_data.last_name
    if update_data.phone_number is not None:
        user.phone_number = update_data.phone_number
    
    # Save changes
    updated_user = await user_repo.update(user)
    
    logger.info(f"User profile updated: {updated_user.email}")
    
    return UserResponse(
        id=updated_user.user_id,
        email=updated_user.email,
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        full_name=f"{updated_user.first_name} {updated_user.last_name}",
        phone_number=updated_user.phone_number,
        tier=getattr(updated_user, 'tier', 5000),
        is_active=getattr(updated_user, 'is_active', True),
        is_admin=getattr(updated_user, 'is_admin', False),
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at,
    )
