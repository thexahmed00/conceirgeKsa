"""SQLAlchemy Service models - Categories, Vendors, and Images."""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Float,
    ForeignKey, Index, LargeBinary, JSON
)
from sqlalchemy.orm import relationship
from src.infrastructure.persistence.models.user import Base


class ServiceCategoryModel(Base):
    """SQLAlchemy model for service categories (restaurant, hotel, etc.)."""
    
    __tablename__ = "service_categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)
    icon_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    vendors = relationship("ServiceVendorModel", back_populates="category", cascade="all, delete-orphan")
    subcategories = relationship("ServiceSubcategoryModel", back_populates="category", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_category_slug', 'slug'),
        Index('idx_category_icon_url', 'icon_url'),
        Index('idx_category_display_order', 'display_order'),
    )
    
    def __repr__(self) -> str:
        return f"<ServiceCategoryModel(id={self.id}, slug={self.slug})>"


class ServiceSubcategoryModel(Base):
    """SQLAlchemy model for service subcategories (e.g., Italian restaurant under Restaurant category)."""
    
    __tablename__ = "service_subcategories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("service_categories.id"), nullable=False)
    slug = Column(String(50), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)
    icon_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    category = relationship("ServiceCategoryModel", back_populates="subcategories")
    
    __table_args__ = (
        Index('idx_subcategory_category_id', 'category_id'),
        Index('idx_subcategory_slug', 'slug'),
        Index('idx_subcategory_display_order', 'display_order'),
    )
    
    def __repr__(self) -> str:
        return f"<ServiceSubcategoryModel(id={self.id}, category_id={self.category_id}, slug={self.slug})>"


class ServiceVendorModel(Base):
    """SQLAlchemy model for service vendors (Cafe Bonjour, Hotel Paradiso, etc.)."""
    
    __tablename__ = "service_vendors"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("service_categories.id"), nullable=False)
    
    # Basic info
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    
    # City/Location
    city = Column(String(100), nullable=True)
    
    # Contact info
    address = Column(String(500), nullable=True)
    phone = Column(String(50), nullable=True)
    website = Column(String(255), nullable=True)
    whatsapp = Column(String(50), nullable=True)
    
    # Rating (0-5)
    rating = Column(Float, nullable=False, default=0.0)
    
    # Type-specific data stored as JSONB
    # Examples:
    # Restaurant: {"cuisine": "Italian", "hours": {...}, "dishes": [...]}
    # Hotel: {"amenities": [...], "rooms": [...], "check_in": "3:00 PM"}
    # Private Jet: {"aircraft": [...]}
    vendor_metadata = Column(JSON, nullable=False, default=dict)
    
    # Status
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("ServiceCategoryModel", back_populates="vendors")
    images = relationship("VendorImageModel", back_populates="vendor", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_vendor_category_id', 'category_id'),
        Index('idx_vendor_is_active', 'is_active'),
        Index('idx_vendor_rating', 'rating'),
        Index('idx_vendor_city', 'city'),
        Index('idx_vendor_created_at', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<ServiceVendorModel(id={self.id}, name={self.name})>"


class VendorImageModel(Base):
    """SQLAlchemy model for vendor images (hero carousel and gallery)."""
    
    __tablename__ = "vendor_images"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    vendor_id = Column(Integer, ForeignKey("service_vendors.id"), nullable=False)
    
    # Image type: 'hero' for carousel, 'gallery' for gallery images
    image_type = Column(String(20), nullable=False)
    
    # Image URLs (S3, Unsplash, etc.)
    image_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    
    # Metadata
    caption = Column(String(255), nullable=True)
    display_order = Column(Integer, nullable=False, default=0)
    
    # Timestamp
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    vendor = relationship("ServiceVendorModel", back_populates="images")
    
    __table_args__ = (
        Index('idx_image_vendor_id', 'vendor_id'),
        Index('idx_image_type', 'image_type'),
        Index('idx_image_vendor_type', 'vendor_id', 'image_type'),
        Index('idx_image_display_order', 'display_order'),
    )
    
    def __repr__(self) -> str:
        return f"<VendorImageModel(id={self.id}, vendor_id={self.vendor_id}, type={self.image_type})>"
