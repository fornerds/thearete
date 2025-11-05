"""Pydantic request schemas for treatment sessions domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Request16(BaseModel):
    """Schema for treatment sessions_request_16"""
    
    treatment_id: int = Field(..., description="시술 ID")
    date: str = Field(..., description="시술 날짜 (YYYY-MM-DD)")
    duration: Optional[int] = Field(None, description="소요시간(분)")
    note: Optional[str] = Field(None, description="특이사항")
    melanin: Optional[int] = Field(None, description="멜라닌 투입량 (0~9)")
    white: Optional[int] = Field(None, description="화이트 투입량 (0~9)")
    red: Optional[int] = Field(None, description="레드 투입량 (0~9)")
    yellow: Optional[int] = Field(None, description="옐로우 투입량 (0~9)")

class Request17(BaseModel):
    """Schema for treatment sessions_request_17"""
    
    treatment_id: Optional[int] = Field(None, description="시술 ID (필터링용)")


class Request18(BaseModel):
    """Schema for treatment sessions_request_18"""
    


class Request19(BaseModel):
    """Schema for treatment sessions_request_19"""
    
    note: Optional[str] = Field(None, description="특이사항")
    duration: Optional[int] = Field(None, description="소요시간(분)")
    date: Optional[str] = Field(None, description="시술 날짜")
    melanin: Optional[int] = Field(None, description="멜라닌 투입량")
    white: Optional[int] = Field(None, description="화이트 투입량")
    red: Optional[int] = Field(None, description="레드 투입량")
    yellow: Optional[int] = Field(None, description="옐로우 투입량")

class Request20(BaseModel):
    """Schema for treatment sessions_request_20"""
    


class Request21(BaseModel):
    """Schema for treatment sessions_request_21"""
    
    is_result_entered: int = Field(..., description="시술 결과 입력 저장 여부 (0 또는 1)")

