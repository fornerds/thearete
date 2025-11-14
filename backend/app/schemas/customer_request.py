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
    class Config:
        json_schema_extra = {
            "example": {
                "name": "김고갱",
                "age": "23",
                "gender": "M",
                "phone": "010-1234-3456",
                "skin_type": "건성",
                "note": "노트 메모,,,"
            }
        }
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
    

class Request11(BaseModel):
    """Schema for customer_request_11 - Update marked status"""
    
    marked: Optional[int] = Field(None, description="상단 고정 여부 (1: 고정, 0: 해제, null: toggle)")


