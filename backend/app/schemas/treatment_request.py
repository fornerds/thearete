"""Pydantic request schemas for treatment domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Request11(BaseModel):
    """Schema for treatment_request_11"""
    
    customer_id: int = Field(..., description="고객 ID")
    name: Optional[str] = Field(None, description="시술명")
    type: Optional[str] = Field(None, description="시술 종류")
    area: Optional[str] = Field(None, description="시술 부위")

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

