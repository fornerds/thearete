"""Pydantic request schemas for shop domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Request1(BaseModel):
    """Schema for shop_request_1"""
    
    name: Optional[str] = Field(None)
    address: Optional[str] = Field(None)
    owner: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    password: Optional[str] = Field(None)

class Request2(BaseModel):
    """Schema for shop_request_2"""
    


class Request3(BaseModel):
    """Schema for shop_request_3"""
    


class Request4(BaseModel):
    """Schema for shop_request_4"""
    
    address: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)

class Request5(BaseModel):
    """Schema for shop_request_5"""
    


