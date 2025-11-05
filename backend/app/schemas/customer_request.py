"""Pydantic request schemas for customer domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Request6(BaseModel):
    """Schema for customer_request_6"""
    
    name: Optional[str] = Field(None)
    age: Optional[int] = Field(None, description="나이 (정수)")
    gender: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    skin_type: Optional[str] = Field(None)
    note: Optional[str] = Field(None)

class Request7(BaseModel):
    """Schema for customer_request_7"""
    


class Request8(BaseModel):
    """Schema for customer_request_8"""
    


class Request9(BaseModel):
    """Schema for customer_request_9"""
    
    skin_type: Optional[str] = Field(None)
    note: Optional[str] = Field(None)

class Request10(BaseModel):
    """Schema for customer_request_10"""
    


