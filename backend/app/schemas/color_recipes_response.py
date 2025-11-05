"""Pydantic response schemas for color recipes domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Response25(BaseModel):
    """Schema for color recipes_response_25"""
    
    recipe_id: Optional[str] = Field(None)
    created_at: Optional[str] = Field(None)

class Response26(BaseModel):
    """Schema for color recipes_response_26"""
    
    melanin: Optional[str] = Field(None)
    white: Optional[str] = Field(None)
    red: Optional[str] = Field(None)
    yellow: Optional[str] = Field(None)

