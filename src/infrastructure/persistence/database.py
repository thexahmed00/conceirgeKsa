"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

from src.config import settings
from src.infrastructure.persistence.models.user import Base
# Import all models so they're registered with Base.metadata
from src.infrastructure.persistence.models.request import RequestModel
from src.infrastructure.persistence.models.conversation import ConversationModel, MessageModel
from src.infrastructure.persistence.models.service import (
    ServiceCategoryModel, ServiceVendorModel, VendorImageModel
)
from src.infrastructure.persistence.models.booking import BookingModel

# Create engine with NullPool for async contexts
engine = create_engine(
    settings.database_url,
    poolclass=NullPool,
    echo=settings.debug,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def init_db() -> None:
    """Initialize database - create all tables."""
    Base.metadata.create_all(bind=engine)


def close_db() -> None:
    """Close database connections."""
    engine.dispose()


def drop_all_tables() -> None:
    """Drop all tables (use with caution)."""
    Base.metadata.drop_all(bind=engine)
