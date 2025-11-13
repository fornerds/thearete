"""Pydantic response schemas for treatment sessions domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any


class SessionImageOutput(BaseModel):
    """세션 이미지 정보."""

    image_id: Optional[str] = Field(None)
    url: Optional[str] = Field(None)
    sequence_no: Optional[int] = Field(None)
    type: Optional[str] = Field(None)

class Response16(BaseModel):
    """Schema for treatment sessions_response_16"""
    
    session_id: Optional[str] = Field(None)
    created_at: Optional[str] = Field(None)

class Response17(BaseModel):
    """Schema for treatment sessions_response_17"""
    
    session_id: Optional[str] = Field(None)
    date: Optional[str] = Field(None)

class Response18(BaseModel):
    """Schema for treatment sessions_response_18"""
    
    session_id: Optional[str] = Field(None)
    duration: Optional[str] = Field(None)
    note: Optional[str] = Field(None)
    images: Optional[List[SessionImageOutput]] = Field(None)

class Response19(BaseModel):
    """Schema for treatment sessions_response_19"""
    
    updated_at: Optional[str] = Field(None)

class Response20(BaseModel):
    """Schema for treatment sessions_response_20"""
    
    deleted_at: Optional[str] = Field(None)

class Response21(BaseModel):
    """Schema for treatment sessions_response_21"""
    
    session_id: Optional[str] = Field(None)
    is_result_entered: Optional[str] = Field(None)
    message: Optional[str] = Field(None)
    images: Optional[List[SessionImageOutput]] = Field(None)

