"""Pydantic response schemas for treatment photos domain."""

from pydantic import BaseModel, Field
from typing import List, Optional

class PhotoMetadata(BaseModel):
    """Shared schema for treatment photo metadata."""

    photo_id: Optional[str] = Field(None)
    treatment_id: Optional[int] = Field(None)
    session_id: Optional[int] = Field(None)
    type: Optional[str] = Field(None)
    image_url: Optional[str] = Field(None)
    thumbnail_url: Optional[str] = Field(None)
    created_at: Optional[str] = Field(None)


class Response27(BaseModel):
    """Schema for treatment photos_response_27"""

    photos: List[PhotoMetadata] = Field(default_factory=list)

class Response28(BaseModel):
    """Schema for treatment photos_response_28"""
    
    photo_id: Optional[str] = Field(None)
    type: Optional[str] = Field(None)
    image_url: Optional[str] = Field(None)
    thumbnail_url: Optional[str] = Field(None)

class Response29(BaseModel):
    """Schema for treatment photos_response_29"""
    
    deleted_at: Optional[str] = Field(None)

