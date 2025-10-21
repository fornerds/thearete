"""Pydantic response schemas for customer domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Response6(BaseModel):
    """Schema for customer_response_6"""
    
    customer_id: Optional[str] = Field(None)
    created_at: Optional[str] = Field(None)

class Response7(BaseModel):
    """Schema for customer_response_7"""
    
    customer_id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)

class Response8(BaseModel):
    """Schema for customer_response_8"""
    
    customer_id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    skin_type: Optional[str] = Field(None)

class Response9(BaseModel):
    """Schema for customer_response_9"""
    
    updated_at: Optional[str] = Field(None)

class Response10(BaseModel):
    """Schema for customer_response_10"""
    
    deleted_at: Optional[str] = Field(None)

