"""Authentication API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.application.user.dto import UserCreateRequest, UserLoginRequest, UserResponse, TokenResponse
from src.application.user.use_cases.user_use_cases import (
    CreateUserUseCase,
    AuthenticateUserUseCase,
    GetUserUseCase,
)
from src.infrastructure.persistence.repositories.user_repository import PostgreSQLUserRepository
from src.infrastructure.web.dependencies import get_db, get_current_user
from src.domain.shared.exceptions import InvalidUserError, DuplicateResourceError
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["authentication"],
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: UserCreateRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Register new user account.
    
    Args:
        request: Registration request with email, password, name
        db: Database session
        
    Returns:
        Created user response
        
    Raises:
        HTTPException 400: If email already exists
        HTTPException 422: If validation fails
    """
    try:
        user_repo = PostgreSQLUserRepository(db)
        use_case = CreateUserUseCase(user_repo)
        user_response = await use_case.execute(request)
        
        logger.info(f"User registered: {user_response.email}")
        
        return user_response
    except DuplicateResourceError as e:
        logger.warning(f"Duplicate registration attempt: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except InvalidUserError as e:
        logger.warning(f"Invalid user registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Authenticate user and return JWT token.
    
    Args:
        request: Login request with email and password
        db: Database session
        
    Returns:
        Token response with access token and user info
        
    Raises:
        HTTPException 401: If credentials invalid
    """
    try:
        user_repo = PostgreSQLUserRepository(db)
        use_case = AuthenticateUserUseCase(user_repo)
        user_response, token = await use_case.execute(request)
        
        logger.info(f"User authenticated: {user_response.email}")
        
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            expires_in=86400,  # 24 hours in seconds
        )
    except InvalidUserError as e:
        logger.warning(f"Failed login attempt: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Get current authenticated user profile.
    
    Args:
        current_user: Current user ID (from JWT token)
        db: Database session
        
    Returns:
        Current user details
        
    Raises:
        HTTPException 404: If user not found
    """
    try:
        user_repo = PostgreSQLUserRepository(db)
        use_case = GetUserUseCase(user_repo)
        user_response = await use_case.execute(current_user)
        
        return user_response
    except InvalidUserError as e:
        logger.warning(f"User not found: {current_user}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error retrieving user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
