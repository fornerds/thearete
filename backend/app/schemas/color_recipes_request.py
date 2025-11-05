"""Pydantic request schemas for color recipes domain."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Request25(BaseModel):
    """Schema for color recipes_request_25 - Color recipe 생성 요청"""
    
    session_id: int = Field(..., description="시술 회차 ID (피부색 측정 데이터 기반으로 AI가 추천)")

class Request26(BaseModel):
    """Schema for color recipes_request_26"""
    


