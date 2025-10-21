"""Pydantic response schemas for shop domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Response1(BaseModel):
    """Schema for shop_response_1"""
    
    shop_id: Optional[str] = Field(None)
    created_at: Optional[str] = Field(None)

class Response2(BaseModel):
    """Schema for shop_response_2"""
    
    shop_id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)

class Response3(BaseModel):
    """Schema for shop_response_3"""
    
    shop_id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    address: Optional[str] = Field(None)
    owner: Optional[str] = Field(None)

class Response4(BaseModel):
    """Schema for shop_response_4"""
    
    updated_at: Optional[str] = Field(None)

class Response5(BaseModel):
    """Schema for shop_response_5"""
    
    deleted_at: Optional[str] = Field(None)

