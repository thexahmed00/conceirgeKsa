"""SQLAlchemy Content models - Banners and Cities."""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Index
)
from src.infrastructure.persistence.models.user import Base


class BannerModel(Base):
    """SQLAlchemy model for promotional banners."""
    
    __tablename__ = "banners"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    image_url = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    link_url = Column(String(500), nullable=True)
    display_order = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_banner_active', 'is_active'),
        Index('idx_banner_display_order', 'display_order'),
    )
    
    def __repr__(self) -> str:
        return f"<BannerModel(id={self.id}, title={self.title})>"


class CityModel(Base):
    """SQLAlchemy model for cities/locations."""
    
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    name_ar = Column(String(100), nullable=True)  # Arabic name
    country = Column(String(100), nullable=False, default="Saudi Arabia")
    display_order = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_city_active', 'is_active'),
        Index('idx_city_display_order', 'display_order'),
        Index('idx_city_name', 'name'),
    )
    
    def __repr__(self) -> str:
        return f"<CityModel(id={self.id}, name={self.name})>"
