"""Pydantic request schemas for treatment photos domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Request27(BaseModel):
    """Schema for treatment photos_request_27"""
    
    treatment_id: int = Field(..., description="시술 ID")
    session_id: Optional[int] = Field(None, description="시술 회차 ID (선택)")
    type: str = Field(..., description="사진 타입 (BEFORE 또는 AFTER)")
    image_url: str = Field(..., description="이미지 URL")

class Request28(BaseModel):
    """Schema for treatment photos_request_28"""
    
    treatment_id: Optional[int] = Field(None, description="시술 ID (필터링용)")
    session_id: Optional[int] = Field(None, description="시술 회차 ID (필터링용)")


class Request29(BaseModel):
    """Schema for treatment photos_request_29"""
    


