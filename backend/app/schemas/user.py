"""User Pydantic schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import BaseSchema, TimestampMixin


class UserBase(BaseModel):
    """Base user schema."""
    
    email: EmailStr = Field(description="User email address")
    username: str = Field(min_length=3, max_length=100, description="Username")
    full_name: Optional[str] = Field(None, max_length=255, description="Full name")
    bio: Optional[str] = Field(None, description="User biography")
    avatar_url: Optional[str] = Field(None, max_length=500, description="Avatar URL")


class UserCreate(UserBase):
    """User creation schema."""
    
    password: str = Field(min_length=8, description="Password")


class UserUpdate(BaseModel):
    """User update schema."""
    
    email: Optional[EmailStr] = Field(None, description="User email address")
    username: Optional[str] = Field(None, min_length=3, max_length=100, description="Username")
    full_name: Optional[str] = Field(None, max_length=255, description="Full name")
    bio: Optional[str] = Field(None, description="User biography")
    avatar_url: Optional[str] = Field(None, max_length=500, description="Avatar URL")
    is_active: Optional[bool] = Field(None, description="User active status")


class UserInDB(UserBase, TimestampMixin):
    """User in database schema."""
    
    id: int = Field(description="User ID")
    is_active: bool = Field(description="User active status")
    is_superuser: bool = Field(description="Superuser status")


class User(UserInDB):
    """User response schema."""
    
    pass


class UserProfile(UserBase):
    """User profile schema for public display."""
    
    id: int = Field(description="User ID")
    is_active: bool = Field(description="User active status")
    created_at: datetime = Field(description="Creation timestamp")
