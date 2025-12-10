"""FastAPI dependency injection setup."""

from typing import Optional, Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.infrastructure.persistence.database import SessionLocal
from src.infrastructure.auth.jwt_handler import get_user_id_from_token
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
