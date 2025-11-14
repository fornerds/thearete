"""Pydantic request schemas for treatment domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class SessionImageInput(BaseModel):
    """이미지 매핑 입력."""

    url: str = Field(..., description="업로드된 이미지 URL")
    sequence_no: Optional[int] = Field(None, description="표시 순서 (0부터 시작)")
    type: Optional[str] = Field(None, description="사진 타입 (BEFORE/AFTER)")

class Request11(BaseModel):
    """Schema for treatment_request_11"""
    
    customer_id: int = Field(..., description="고객 ID")
    name: Optional[str] = Field(None, description="시술명")
    type: Optional[str] = Field(None, description="시술 종류")
    area: Optional[str] = Field(None, description="시술 부위")
    images: Optional[List[SessionImageInput]] = Field(default_factory=list, description="시술 1회차에 연결할 이미지 목록")

class Request12(BaseModel):
    """Schema for treatment_request_12"""
    
    customer_id: Optional[int] = Field(None, description="고객 ID (필터링용)")


class Request13(BaseModel):
    """Schema for treatment_request_13"""
    


class Request14(BaseModel):
    """Schema for treatment_request_14"""
    
    name: Optional[str] = Field(None, description="시술명")
    type: Optional[str] = Field(None, description="시술 종류")
    area: Optional[str] = Field(None, description="시술 부위")

class Request15(BaseModel):
    """Schema for treatment_request_15"""
    
    is_completed: bool = Field(..., description="완료 여부")

