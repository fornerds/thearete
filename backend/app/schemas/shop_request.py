"""Pydantic request schemas for shop domain."""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any

class Request1(BaseModel):
    """Schema for shop_request_1"""
    
    name: Optional[str] = Field(None)
    address: Optional[str] = Field(None)
    owner: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    password: Optional[str] = Field(None, min_length=6, description="비밀번호 (최대 72바이트)")
    
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        """비밀번호가 72바이트를 초과하지 않도록 검증"""
        if v is not None:
            password_bytes = v.encode('utf-8')
            if len(password_bytes) > 72:
                raise ValueError(
                    f"비밀번호는 최대 72바이트까지 허용됩니다. "
                    f"현재 비밀번호는 {len(password_bytes)}바이트입니다."
                )
            if len(password_bytes) < 6:
                raise ValueError("비밀번호는 최소 6바이트 이상이어야 합니다.")
        return v

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
    


