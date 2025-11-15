"""Pydantic request schemas for treatment photos domain."""

from pydantic import BaseModel, Field
from typing import List, Optional


class SessionImagePayload(BaseModel):
    url: str = Field(..., description="업로드된 이미지 URL")
    type: Optional[str] = Field(None, description="사진 타입 (BEFORE/AFTER)")


class Request27(BaseModel):
    """Schema for attaching treatment session images."""

    treatment_id: int = Field(..., description="시술 ID")
    session_id: int = Field(..., description="시술 회차 ID")
    images: List[SessionImagePayload] = Field(..., description="세션에 연결할 이미지 목록")

class Request28(BaseModel):
    """Schema for treatment photos_request_28"""
    
    treatment_id: Optional[int] = Field(None, description="시술 ID (필터링용)")
    session_id: Optional[int] = Field(None, description="시술 회차 ID (필터링용)")


class Request29(BaseModel):
    """Schema for treatment photos_request_29"""
    


