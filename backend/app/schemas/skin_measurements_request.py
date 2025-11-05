"""Pydantic request schemas for skin measurements domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Request22(BaseModel):
    """Schema for skin measurements_request_22"""
    
    session_id: int = Field(..., description="시술 회차 ID")
    type: str = Field(..., description="측정 타입 (NORMAL 또는 LESION)")
    L: float = Field(..., description="L 값")
    a: float = Field(..., description="a 값")
    b: float = Field(..., description="b 값")
    measurement_point: Optional[str] = Field(None, description="측정 위치")
    measured_at: Optional[str] = Field(None, description="측정 시각 (ISO format)")

class Request23(BaseModel):
    """Schema for skin measurements_request_23"""
    
    session_id: Optional[int] = Field(None, description="시술 회차 ID (필터링용)")


class Request24(BaseModel):
    """Schema for skin measurements_request_24"""
    


