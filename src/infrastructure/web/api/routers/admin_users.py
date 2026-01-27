"""Admin API endpoints for user management."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path

from src.application.user.dto.user_dto import (
    UserCreateRequest,
    UserResponse,
    AdminUserUpdateRequest,
    UserListResponse,
    DeleteAccountResponse,
)
from src.application.user.use_cases.user_use_cases import (
    ListAllUsersUseCase,
    GetUserByIdUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
    CreateAdminUserUseCase,
)
from src.domain.shared.exceptions import ResourceNotFoundError, DuplicateResourceError, InvalidUserError
from src.infrastructure.web.dependencies import (
    get_current_admin_user,
    get_list_all_users_use_case,
    get_user_by_id_use_case,
    get_update_user_use_case,
    get_delete_user_use_case,
    get_create_admin_user_use_case,
)
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/admin/users",
    tags=["admin-users"],
)


@router.get("", response_model=UserListResponse)
def list_all_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum records to return"),
    admin_id: int = Depends(get_current_admin_user),
    use_case: ListAllUsersUseCase = Depends(get_list_all_users_use_case),
) -> UserListResponse:
    """List all users with pagination (admin only).
    
    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum records to return (default: 20, max: 100)
        admin_id: Current admin user ID (from auth)
        use_case: ListAllUsersUseCase dependency
        
    Returns:
        UserListResponse with paginated users and total count
    """
    try:
        logger.info(f"Admin {admin_id} listing all users: skip={skip}, limit={limit}")
        return use_case.execute(skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list users"
        )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int = Path(..., ge=1, description="User ID"),
    admin_id: int = Depends(get_current_admin_user),
    use_case: GetUserByIdUseCase = Depends(get_user_by_id_use_case),
) -> UserResponse:
    """Get a specific user by ID (admin only).
    
    Args:
        user_id: User ID to retrieve
        admin_id: Current admin user ID (from auth)
        use_case: GetUserByIdUseCase dependency
        
    Returns:
        UserResponse with user details
        
    Raises:
        HTTPException 404: If user not found
    """
    try:
        logger.info(f"Admin {admin_id} fetching user {user_id}")
        return use_case.execute(user_id)
    except ResourceNotFoundError as e:
        logger.warning(f"User {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error fetching user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user"
        )


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    request: UserCreateRequest,
    is_admin: bool = Query(False, description="Create as admin user"),
    admin_id: int = Depends(get_current_admin_user),
    use_case: CreateAdminUserUseCase = Depends(get_create_admin_user_use_case),
) -> UserResponse:
    """Create a new user (admin only).
    
    Args:
        request: User creation request with email, password, name, phone
        is_admin: Whether to create as admin user (default: False)
        admin_id: Current admin user ID (from auth)
        use_case: CreateAdminUserUseCase dependency
        
    Returns:
        UserResponse with created user details
        
    Raises:
        HTTPException 400: If email already exists
        HTTPException 500: If creation fails
    """
    try:
        logger.info(f"Admin {admin_id} creating user: {request.email} (admin={is_admin})")
        return use_case.execute(request, is_admin=is_admin)
    except DuplicateResourceError as e:
        logger.warning(f"Duplicate user creation attempt: {request.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int = Path(..., ge=1, description="User ID to update"),
    request: AdminUserUpdateRequest = ...,
    admin_id: int = Depends(get_current_admin_user),
    use_case: UpdateUserUseCase = Depends(get_update_user_use_case),
) -> UserResponse:
    """Update user details (admin only).
    
    Can update: first_name, last_name, phone_number, tier, is_active, is_admin
    
    Args:
        user_id: User ID to update
        request: Update request with fields to modify
        admin_id: Current admin user ID (from auth)
        use_case: UpdateUserUseCase dependency
        
    Returns:
        Updated UserResponse
        
    Raises:
        HTTPException 404: If user not found
        HTTPException 500: If update fails
    """
    try:
        logger.info(f"Admin {admin_id} updating user {user_id}")
        return use_case.execute(user_id, request)
    except ResourceNotFoundError as e:
        logger.warning(f"User {user_id} not found for update")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )


@router.delete("/{user_id}", response_model=DeleteAccountResponse)
def delete_user(
    user_id: int = Path(..., ge=1, description="User ID to delete"),
    admin_id: int = Depends(get_current_admin_user),
    use_case: DeleteUserUseCase = Depends(get_delete_user_use_case),
) -> DeleteAccountResponse:
    """Delete a user (admin only).
    
    Args:
        user_id: User ID to delete
        admin_id: Current admin user ID (from auth)
        use_case: DeleteUserUseCase dependency
        
    Returns:
        DeleteAccountResponse confirming deletion
        
    Raises:
        HTTPException 404: If user not found
        HTTPException 500: If deletion fails
    """
    try:
        logger.info(f"Admin {admin_id} deleting user {user_id}")
        return use_case.execute(user_id)
    except ResourceNotFoundError as e:
        logger.warning(f"User {user_id} not found for deletion")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidUserError as e:
        logger.error(f"Error deleting user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error deleting user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )
