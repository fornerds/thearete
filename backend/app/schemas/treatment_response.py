"""Pydantic response schemas for treatment domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Response11(BaseModel):
    """Schema for treatment_response_11"""
    
    treatment_id: str = Field(..., description="시술 ID")
    created_at: Optional[str] = Field(None, description="생성일시")

class Response12(BaseModel):
    """Schema for treatment_response_12"""
    
    treatments: List[dict] = Field(default_factory=list, description="시술 목록")

class Response13(BaseModel):
    """Schema for treatment_response_13"""
    
    treatment_id: str = Field(..., description="시술 ID")
    customer_id: int = Field(..., description="고객 ID")
    name: Optional[str] = Field(None, description="시술명")
    type: Optional[str] = Field(None, description="시술 종류")
    area: Optional[str] = Field(None, description="시술 부위")
    is_completed: Optional[bool] = Field(None, description="완료 여부")
    created_at: Optional[str] = Field(None, description="생성일시")
    updated_at: Optional[str] = Field(None, description="수정일시")
    sessions: Optional[List[dict]] = Field(default_factory=list, description="시술 회차 목록 (이미지 포함)")

class Response14(BaseModel):
    """Schema for treatment_response_14"""
    
    updated_at: Optional[str] = Field(None, description="수정일시")

class Response15(BaseModel):
    """Schema for treatment_response_15"""
    
    message: str = Field(..., description="완료 처리 메시지")

