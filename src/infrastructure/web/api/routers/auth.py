"""Authentication API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.user.dto.user_dto import (
    TokenResponse,
    UserCreateRequest,
    UserLoginRequest,
    UserResponse,
)
from src.application.user.use_cases.user_use_cases import (
    CreateUserUseCase,
    AuthenticateUserUseCase,
    GetUserUseCase,
)
from src.infrastructure.web.dependencies import (
    get_authenticate_user_use_case,
    get_create_user_use_case,
    get_current_user,
    get_user_use_case,
)
from src.domain.shared.exceptions import InvalidUserError, DuplicateResourceError
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["authentication"],
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    request: UserCreateRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
) -> UserResponse:

    try:
        user_response = use_case.execute(request)
        
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
def login(
    request: UserLoginRequest,
    use_case: AuthenticateUserUseCase = Depends(get_authenticate_user_use_case),
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
        user_response, token = use_case.execute(request)
        
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
def get_current_user_profile(
    current_user: int = Depends(get_current_user),
    use_case: GetUserUseCase = Depends(get_user_use_case),
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
        user_response = use_case.execute(current_user)
        
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
