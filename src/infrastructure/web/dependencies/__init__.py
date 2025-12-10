"""FastAPI dependencies."""

from src.infrastructure.web.dependencies.injection import get_db, get_current_user, get_optional_user

__all__ = ["get_db", "get_current_user", "get_optional_user"]
