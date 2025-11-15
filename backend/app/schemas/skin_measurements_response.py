"""Pydantic response schemas for skin measurements domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Response22(BaseModel):
    """Schema for skin measurements_response_22"""
    
    measurement_id: Optional[str] = Field(None)
    created_at: Optional[str] = Field(None)
    melanin: Optional[int] = Field(None, description="추론된 멜라닌 투입량 (0~9)")
    white: Optional[int] = Field(None, description="추론된 화이트 투입량 (0~9)")
    red: Optional[int] = Field(None, description="추론된 레드 투입량 (0~9)")
    yellow: Optional[int] = Field(None, description="추론된 옐로우 투입량 (0~9)")

class Response23(BaseModel):
    """Schema for skin measurements_response_23"""
    
    L: Optional[str] = Field(None)
    a: Optional[str] = Field(None)
    b: Optional[str] = Field(None)
    type: Optional[str] = Field(None)
    melanin: Optional[int] = Field(None)
    white: Optional[int] = Field(None)
    red: Optional[int] = Field(None)
    yellow: Optional[int] = Field(None)

class Response24(BaseModel):
    """Schema for skin measurements_response_24"""
    
    deleted_at: Optional[str] = Field(None)

