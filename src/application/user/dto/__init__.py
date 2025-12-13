"""User DTOs - Data Transfer Objects for API contracts."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    """Request DTO for user registration."""
    
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Password (min 8 chars)")
    first_name: str = Field(..., min_length=1, description="First name")
    last_name: str = Field(..., min_length=1, description="Last name")
    phone_number: Optional[str] = Field(None, description="Phone number")


class UserLoginRequest(BaseModel):
    """Request DTO for user login."""
    
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserResponse(BaseModel):
    """Response DTO for user data (no sensitive info)."""
    
    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    full_name: str = Field(..., description="Full name")
    phone_number: Optional[str] = Field(None, description="Phone number")
    tier: int = Field(..., description="User tier (5000, 25000, 100000)")
    is_active: bool = Field(..., description="Whether user is active")
    created_at: datetime = Field(..., description="Account creation date")
    updated_at: datetime = Field(..., description="Last update date")
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Response DTO for JWT token."""
    
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Expiration time in seconds")


class UserUpdateRequest(BaseModel):
    """Request DTO for updating user profile."""
    
    phone_number: Optional[str] = Field(None, description="Phone number")
    first_name: Optional[str] = Field(None, min_length=1, description="First name")
    last_name: Optional[str] = Field(None, min_length=1, description="Last name")
