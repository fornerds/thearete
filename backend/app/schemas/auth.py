"""Authentication related Pydantic schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Access token expiration time in seconds")
    refresh_expires_in: int = Field(..., description="Refresh token expiration time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600,
                "refresh_expires_in": 604800
            }
        }


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")
    remember_me: bool = Field(False, description="Whether to extend token expiration")
    device_info: Optional[str] = Field(None, description="Device information for session tracking")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "password123",
                "remember_me": False,
                "device_info": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        }


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str = Field(..., description="Valid refresh token")
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class LogoutRequest(BaseModel):
    """Logout request schema."""
    refresh_token: Optional[str] = Field(None, description="Refresh token to revoke")
    revoke_all: bool = Field(False, description="Whether to revoke all user tokens")
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "revoke_all": False
            }
        }


class UserProfile(BaseModel):
    """User profile response schema."""
    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    username: str = Field(..., description="Username")
    full_name: Optional[str] = Field(None, description="Full name")
    is_active: bool = Field(..., description="Whether user is active")
    is_superuser: bool = Field(..., description="Whether user is superuser")
    bio: Optional[str] = Field(None, description="User bio")
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    created_at: datetime = Field(..., description="Account creation time")
    updated_at: datetime = Field(..., description="Last update time")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "is_active": True,
                "is_superuser": False,
                "bio": "Software developer",
                "avatar_url": "https://example.com/avatar.jpg",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }


class TokenInfo(BaseModel):
    """Token information schema."""
    token_id: int = Field(..., description="Token ID")
    token_type: str = Field(..., description="Token type")
    is_revoked: bool = Field(..., description="Whether token is revoked")
    expires_at: datetime = Field(..., description="Token expiration time")
    created_at: datetime = Field(..., description="Token creation time")
    revoked_at: Optional[datetime] = Field(None, description="Token revocation time")
    device_info: Optional[str] = Field(None, description="Device information")
    session_id: Optional[str] = Field(None, description="Session ID")
    
    class Config:
        from_attributes = True


class UserSessions(BaseModel):
    """User sessions response schema."""
    active_sessions: int = Field(..., description="Number of active sessions")
    sessions: list[TokenInfo] = Field(..., description="List of user sessions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "active_sessions": 2,
                "sessions": [
                    {
                        "token_id": 1,
                        "token_type": "refresh",
                        "is_revoked": False,
                        "expires_at": "2024-01-08T00:00:00Z",
                        "created_at": "2024-01-01T00:00:00Z",
                        "device_info": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                        "session_id": "sess_123456"
                    }
                ]
            }
        }


class ShopLoginRequest(BaseModel):
    """Shop login request schema."""
    email: EmailStr = Field(..., description="Shop email address")
    password: str = Field(..., min_length=6, description="Shop password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "skincare1@skin.com",
                "password": "qwer1234"
            }
        }


class ShopLoginResponse(BaseModel):
    """Shop login response schema."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    shop_id: int = Field(..., description="Shop ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "shop_id": 1
            }
        }


class ShopLogoutRequest(BaseModel):
    """Shop logout request schema."""
    refresh_token: str = Field(..., description="Refresh token to revoke")
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class ShopProfile(BaseModel):
    """Shop profile response schema."""
    id: int = Field(..., description="Shop ID")
    name: Optional[str] = Field(None, description="Shop name")
    address: Optional[str] = Field(None, description="Shop address")
    owner_name: Optional[str] = Field(None, description="Owner name")
    phone: Optional[str] = Field(None, description="Phone number")
    email: Optional[str] = Field(None, description="Email address")
    last_login_at: Optional[datetime] = Field(None, description="Last login time")
    created_at: Optional[datetime] = Field(None, description="Account creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "피부샵1",
                "address": "경기도 성남시 분당구 111",
                "owner_name": "김김김",
                "phone": "010-2003-0303",
                "email": "skincare1@skin.com",
                "last_login_at": "2024-01-01T00:00:00Z",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }