"""Pydantic response schemas for skin measurements domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Response22(BaseModel):
    """Schema for skin measurements_response_22"""
    
    measurement_id: Optional[str] = Field(None)
    created_at: Optional[str] = Field(None)

class Response23(BaseModel):
    """Schema for skin measurements_response_23"""
    
    L: Optional[str] = Field(None)
    a: Optional[str] = Field(None)
    b: Optional[str] = Field(None)
    type: Optional[str] = Field(None)

class Response24(BaseModel):
    """Schema for skin measurements_response_24"""
    
    deleted_at: Optional[str] = Field(None)

