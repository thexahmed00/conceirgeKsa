"""User authentication use cases."""

from datetime import datetime, timedelta
from typing import Tuple

from src.application.user.dto.user_dto import (
    UserCreateRequest,
    UserLoginRequest,
    UserResponse,
    ChangePasswordRequest,
    ChangePasswordResponse,
    DeleteAccountResponse,
    AdminUserUpdateRequest,
    UserListResponse,
)
from src.domain.user.entities.user import User
from src.domain.user.repository.user_repository import UserRepository
from src.domain.shared.exceptions import InvalidUserError, DuplicateResourceError, ResourceNotFoundError
from src.shared.utils.password_utils import hash_password
from src.infrastructure.auth.jwt_handler import create_access_token
import logging

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    """User registration use case."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def execute(self, request: UserCreateRequest) -> UserResponse:
        """Create new user account.
        
        Args:
            request: User registration request DTO
            
        Returns:
            UserResponse DTO
            
        Raises:
            DuplicateResourceError: If email already exists
        """
        # Check for duplicate email
        existing_user = self._user_repository.find_by_email(request.email)
        if existing_user:
            raise DuplicateResourceError(f"User with email {request.email} already exists")

        # Hash password
        hashed_pwd = hash_password(request.password)

        # Create User entity
        user = User(
            user_id=999999,  # Temporary, will be replaced by DB
            email=request.email,
            hashed_password=hashed_pwd,
            first_name=request.first_name,
            last_name=request.last_name,
            phone_number=request.phone_number,
        )

        # Save user
        saved_user = self._user_repository.save(user)

        # Simple logging
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"User created: {saved_user.email}")

        # Return response DTO
        return UserResponse(
            id=saved_user.user_id,
            email=saved_user.email,
            first_name=saved_user.first_name,
            last_name=saved_user.last_name,
            full_name=f"{saved_user.first_name} {saved_user.last_name}",
            phone_number=saved_user.phone_number,
            tier=getattr(saved_user, 'tier', 5000),
            is_active=getattr(saved_user, 'is_active', True),
            created_at=saved_user.created_at,
            updated_at=saved_user.updated_at,
        )


class ListAllUsersUseCase:
    """Admin use case to list all users with pagination."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def execute(self, skip: int = 0, limit: int = 20) -> UserListResponse:
        """List all users.
        
        Args:
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            UserListResponse with paginated users
        """
        users = self._user_repository.find_all(skip=skip, limit=limit)
        total = self._user_repository.count_all()
        
        user_responses = [
            UserResponse(
                id=user.user_id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                full_name=f"{user.first_name} {user.last_name}",
                phone_number=user.phone_number,
                tier=getattr(user, 'tier', 5000),
                is_active=getattr(user, 'is_active', True),
                is_admin=getattr(user, 'is_admin', False),
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            for user in users
        ]
        
        return UserListResponse(
            items=user_responses,
            total=total,
            skip=skip,
            limit=limit,
        )


class GetUserByIdUseCase:
    """Admin use case to get a specific user by ID."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def execute(self, user_id: int) -> UserResponse:
        """Get user by ID.
        
        Args:
            user_id: User ID to retrieve
            
        Returns:
            UserResponse DTO
            
        Raises:
            ResourceNotFoundError: If user not found
        """
        user = self._user_repository.find_by_id(user_id)
        if not user:
            raise ResourceNotFoundError(f"User {user_id} not found")

        return UserResponse(
            id=user.user_id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=f"{user.first_name} {user.last_name}",
            phone_number=user.phone_number,
            tier=getattr(user, 'tier', 5000),
            is_active=getattr(user, 'is_active', True),
            is_admin=getattr(user, 'is_admin', False),
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class UpdateUserUseCase:
    """Admin use case to update user details."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def execute(self, user_id: int, request: AdminUserUpdateRequest) -> UserResponse:
        """Update user details.
        
        Args:
            user_id: User ID to update
            request: Update request DTO
            
        Returns:
            Updated UserResponse DTO
            
        Raises:
            ResourceNotFoundError: If user not found
        """
        user = self._user_repository.find_by_id(user_id)
        if not user:
            raise ResourceNotFoundError(f"User {user_id} not found")

        # Update fields if provided
        if request.first_name is not None:
            user.first_name = request.first_name
        if request.last_name is not None:
            user.last_name = request.last_name
        if request.phone_number is not None:
            user.phone_number = request.phone_number
        if request.tier is not None:
            user.tier = request.tier
        if request.is_active is not None:
            user.is_active = request.is_active
        if request.is_admin is not None:
            user.is_admin = request.is_admin

        # Save changes
        updated_user = self._user_repository.update(user)
        
        logger.info(f"User updated: {updated_user.email}")

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


class DeleteUserUseCase:
    """Admin use case to delete a user."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def execute(self, user_id: int) -> DeleteAccountResponse:
        """Delete a user.
        
        Args:
            user_id: User ID to delete
            
        Returns:
            DeleteAccountResponse DTO
            
        Raises:
            ResourceNotFoundError: If user not found
        """
        user = self._user_repository.find_by_id(user_id)
        if not user:
            raise ResourceNotFoundError(f"User {user_id} not found")

        success = self._user_repository.delete(user_id)

        if success:
            logger.info(f"User deleted by admin: {user.email}")
            return DeleteAccountResponse(
                success=True,
                message="User deleted successfully"
            )
        else:
            raise InvalidUserError("Failed to delete user")


class CreateAdminUserUseCase:
    """Admin use case to create a user with optional admin privileges."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def execute(self, request: UserCreateRequest, is_admin: bool = False) -> UserResponse:
        """Create new user as admin.
        
        Args:
            request: User creation request DTO
            is_admin: Whether to create as admin user
            
        Returns:
            UserResponse DTO
            
        Raises:
            DuplicateResourceError: If email already exists
        """
        # Check for duplicate email
        existing_user = self._user_repository.find_by_email(request.email)
        if existing_user:
            raise DuplicateResourceError(f"User with email {request.email} already exists")

        # Hash password
        hashed_pwd = hash_password(request.password)

        # Create User entity
        user = User(
            user_id=999999,  # Temporary, will be replaced by DB
            email=request.email,
            hashed_password=hashed_pwd,
            first_name=request.first_name,
            last_name=request.last_name,
            phone_number=request.phone_number,
        )
        user.is_admin = is_admin

        # Save to database
        saved_user = self._user_repository.save(user)

        logger.info(f"User created by admin: {saved_user.email} (admin={is_admin})")

        # Return response DTO
        return UserResponse(
            id=saved_user.user_id,
            email=saved_user.email,
            first_name=saved_user.first_name,
            last_name=saved_user.last_name,
            full_name=f"{saved_user.first_name} {saved_user.last_name}",
            phone_number=saved_user.phone_number,
            tier=getattr(saved_user, 'tier', 5000),
            is_active=getattr(saved_user, 'is_active', True),
            is_admin=getattr(saved_user, 'is_admin', False),
            created_at=saved_user.created_at,
            updated_at=saved_user.updated_at,
        )


class AuthenticateUserUseCase:
    """User login use case."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def execute(self, request: UserLoginRequest) -> Tuple[UserResponse, str]:
        """Authenticate user with email and password.
        
        Args:
            request: Login request DTO (email, password)
            
        Returns:
            Tuple of (UserResponse DTO, JWT token)
            
        Raises:
            InvalidUserError: If email not found or password incorrect
        """
        # Find user by email
        user = self._user_repository.find_by_email(request.email)
        if not user:
            raise InvalidUserError(f"User with email {request.email} not found")

        # Verify password
        if not user.authenticate(request.password):
            raise InvalidUserError("Invalid password")

        # Generate JWT token (include is_admin flag)
        token = create_access_token(
            data={
                "sub": str(user.user_id),
                "email": user.email,
                "is_admin": getattr(user, 'is_admin', False),
            },
            expires_delta=timedelta(hours=24),
        )

        # Simple logging
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"User authenticated: {user.email}")

        # Return response
        return (
            UserResponse(
                id=user.user_id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                full_name=f"{user.first_name} {user.last_name}",
                phone_number=user.phone_number,
                tier=getattr(user, 'tier', 5000),
                is_active=getattr(user, 'is_active', True),
                created_at=user.created_at,
                updated_at=user.updated_at,
            ),
            token,
        )


class GetUserUseCase:
    """Retrieve user by ID."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def execute(self, user_id: int) -> UserResponse:
        """Get user by ID.
        
        Args:
            user_id: User ID to retrieve
            
        Returns:
            UserResponse DTO
            
        Raises:
            InvalidUserError: If user not found
        """
        user = self._user_repository.find_by_id(user_id)
        if not user:
            raise InvalidUserError(f"User {user_id} not found")

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
            updated_at=user.updated_at,
        )


class ChangePasswordUseCase:
    """Change user password use case."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def execute(self, user_id: int, request: ChangePasswordRequest) -> ChangePasswordResponse:
        """Change user password.
        
        Args:
            user_id: User ID
            request: Change password request DTO
            
        Returns:
            ChangePasswordResponse DTO
            
        Raises:
            InvalidUserError: If user not found or current password incorrect
        """
        user = self._user_repository.find_by_id(user_id)
        if not user:
            raise InvalidUserError(f"User {user_id} not found")

        # Verify current password
        if not user.authenticate(request.current_password):
            raise InvalidUserError("Current password is incorrect")

        # Hash new password and update
        new_hashed_pwd = hash_password(request.new_password)
        user.hashed_password = new_hashed_pwd

        # Save updated user
        self._user_repository.update(user)

        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Password changed for user: {user.email}")

        return ChangePasswordResponse(
            success=True,
            message="Password changed successfully"
        )


class DeleteAccountUseCase:
    """Delete user account use case."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def execute(self, user_id: int) -> DeleteAccountResponse:
        """Delete user account.
        
        Args:
            user_id: User ID to delete
            
        Returns:
            DeleteAccountResponse DTO
            
        Raises:
            InvalidUserError: If user not found
        """
        user = self._user_repository.find_by_id(user_id)
        if not user:
            raise InvalidUserError(f"User {user_id} not found")

        # Delete user
        success = self._user_repository.delete(user_id)

        import logging
        logger = logging.getLogger(__name__)
        
        if success:
            logger.info(f"Account deleted for user: {user.email}")
            return DeleteAccountResponse(
                success=True,
                message="Account deleted successfully"
            )
        else:
            logger.error(f"Failed to delete account for user: {user.email}")
            raise InvalidUserError("Failed to delete account")
