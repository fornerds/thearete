"""Pydantic response schemas for customer domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Response6(BaseModel):
    """Schema for customer_response_6"""
    
    customer_id: Optional[str] = Field(None)
    created_at: Optional[str] = Field(None)

class TreatmentSessionImageInfo(BaseModel):
    """Detailed info for treatment session images."""

    image_id: Optional[str] = Field(None)
    url: Optional[str] = Field(None)
    thumbnail_url: Optional[str] = Field(None)
    sequence_no: Optional[int] = Field(None)
    type: Optional[str] = Field(None)


class TreatmentSessionSummary(BaseModel):
    """Summary of a treatment session."""
    
    treatment_session_id: Optional[str] = Field(None)
    treatment_date: Optional[str] = Field(None)
    duration_minutes: Optional[int] = Field(None)
    is_completed: Optional[bool] = Field(None)
    before_images: List[TreatmentSessionImageInfo] = Field(default_factory=list)
    after_images: List[TreatmentSessionImageInfo] = Field(default_factory=list)


class TreatmentSummary(BaseModel):
    """Summary of a customer's treatment."""
    
    treatment_id: Optional[str] = Field(None)
    type: Optional[str] = Field(None)
    area: Optional[str] = Field(None)
    is_completed: Optional[bool] = Field(None)
    sessions: List[TreatmentSessionSummary] = Field(default_factory=list)


class Response7Customer(BaseModel):
    """Single customer summary for list response."""
    
    customer_id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    gender: Optional[str] = Field(None)
    age: Optional[int] = Field(None)
    skin_type: Optional[str] = Field(None)
    marked: Optional[int] = Field(None, description="상단 고정 여부 (1: 고정, 0 또는 null: 일반)")
    latest_update_time: Optional[str] = Field(None, description="최신 업데이트 시간 (ISO format)")
    treatments: List[TreatmentSummary] = Field(default_factory=list)


class Response7(BaseModel):
    """Schema for customer_request_7"""
    
    customers: List[Response7Customer] = Field(default_factory=list)

class Response8(BaseModel):
    """Schema for customer_response_8"""
    
    customer_id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    gender: Optional[str] = Field(None)
    age: Optional[int] = Field(None)
    skin_type: Optional[str] = Field(None)
    marked: Optional[int] = Field(None, description="상단 고정 여부 (1: 고정, 0 또는 null: 일반)")
    latest_update_time: Optional[str] = Field(None, description="최신 업데이트 시간 (ISO format)")
    treatments: List[TreatmentSummary] = Field(default_factory=list)

class Response9(BaseModel):
    """Schema for customer_response_9"""
    
    updated_at: Optional[str] = Field(None)

class Response10(BaseModel):
    """Schema for customer_response_10"""
    
    deleted_at: Optional[str] = Field(None)

class Response11(BaseModel):
    """Schema for customer_response_11 - Update marked status response"""
    
    customer_id: Optional[str] = Field(None)
    marked: Optional[int] = Field(None, description="상단 고정 여부 (1: 고정, 0 또는 null: 일반)")
    updated_at: Optional[str] = Field(None)

