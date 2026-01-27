"""User DTOs - Data Transfer Objects for API contracts.

These are separate from domain entities. They handle serialization/deserialization
and API request/response formatting.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    """Request DTO for user registration."""
    
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Password (min 8 chars)")
    first_name: str = Field(..., min_length=1, description="First name")
    last_name: str = Field(..., min_length=1, description="Last name")
    phone_number: Optional[str] = Field(None, description="Phone number")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePassword123",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+966501234567",
            }
        }


class UserLoginRequest(BaseModel):
    """Request DTO for user login."""
    
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePassword123",
            }
        }


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
    is_admin: bool = Field(default=False, description="Whether user is an admin")
    created_at: datetime = Field(..., description="Account creation date")
    updated_at: datetime = Field(..., description="Last update date")
    
    class Config:
        from_attributes = True  # orm_mode in Pydantic v2
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "full_name": "John Doe",
                "phone_number": "+966501234567",
                "tier": 5000,
                "is_active": True,
                "is_admin": False,
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-15T15:30:00Z",
            }
        }


class UserUpdateRequest(BaseModel):
    """Request DTO for updating user profile."""
    
    phone_number: Optional[str] = Field(None, description="Phone number")
    first_name: Optional[str] = Field(None, min_length=1, description="First name")
    last_name: Optional[str] = Field(None, min_length=1, description="Last name")
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+966501234567",
                "first_name": "John",
                "last_name": "Doe",
            }
        }


class AdminUserUpdateRequest(BaseModel):
    """Request DTO for admin to update user (can change admin status)."""
    
    first_name: Optional[str] = Field(None, min_length=1, description="First name")
    last_name: Optional[str] = Field(None, min_length=1, description="Last name")
    phone_number: Optional[str] = Field(None, description="Phone number")
    tier: Optional[int] = Field(None, ge=5000, description="User tier")
    is_active: Optional[bool] = Field(None, description="Whether user is active")
    is_admin: Optional[bool] = Field(None, description="Whether user is an admin")
    
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Jane",
                "last_name": "Smith",
                "phone_number": "+966501234567",
                "tier": 25000,
                "is_active": True,
                "is_admin": False,
            }
        }


class UserListResponse(BaseModel):
    """Response DTO for list of users with pagination."""
    
    items: List[UserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Maximum records returned")
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "email": "john.doe@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "full_name": "John Doe",
                        "phone_number": "+966501234567",
                        "tier": 5000,
                        "is_active": True,
                        "is_admin": False,
                        "created_at": "2024-01-01T12:00:00Z",
                        "updated_at": "2024-01-15T15:30:00Z",
                    }
                ],
                "total": 50,
                "skip": 0,
                "limit": 20,
            }
        }


class ChangePasswordRequest(BaseModel):
    """Request DTO for changing password."""
    
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password (min 8 chars)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "OldPassword123",
                "new_password": "NewSecurePassword456",
            }
        }


class ChangePasswordResponse(BaseModel):
    """Response DTO for password change."""
    
    success: bool = Field(..., description="Whether password was changed successfully")
    message: str = Field(..., description="Success message")


class DeleteAccountResponse(BaseModel):
    """Response DTO for account deletion."""
    
    success: bool = Field(..., description="Whether account was deleted successfully")
    message: str = Field(..., description="Deletion message")


class TokenResponse(BaseModel):
    """Response DTO for JWT token."""
    
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Expiration time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 86400,
            }
        }
