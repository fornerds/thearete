"""Pydantic request schemas for color recipes domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Request25(BaseModel):
    """Schema for color recipes_request_25"""
    
    session_id: int = Field(..., description="시술 회차 ID")
    melanin: int = Field(..., description="멜라닌 투입량 (0~9)")
    white: int = Field(..., description="화이트 투입량 (0~9)")
    red: int = Field(..., description="레드 투입량 (0~9)")
    yellow: int = Field(..., description="옐로우 투입량 (0~9)")

class Request26(BaseModel):
    """Schema for color recipes_request_26"""
    


