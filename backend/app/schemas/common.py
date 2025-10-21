"""Common Pydantic schemas for API responses."""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from enum import Enum

from pydantic import BaseModel, Field


class ErrorCode(str, Enum):
    """Standard error codes."""
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTEGRITY_ERROR = "INTEGRITY_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    TOKEN_INVALID = "TOKEN_INVALID"
    USER_INACTIVE = "USER_INACTIVE"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"


class ErrorDetail(BaseModel):
    """Error detail for validation errors."""
    field: Optional[str] = Field(None, description="Field name that caused the error")
    message: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")


class ErrorResponse(BaseModel):
    """Standard error response format."""
    success: bool = Field(False, description="Always false for error responses")
    error: ErrorCode = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[List[ErrorDetail]] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
    path: Optional[str] = Field(None, description="Request path that caused the error")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "VALIDATION_ERROR",
                "message": "Validation failed",
                "details": [
                    {
                        "field": "email",
                        "message": "Invalid email format",
                        "code": "invalid_email"
                    }
                ],
                "timestamp": "2024-01-01T00:00:00Z",
                "path": "/api/v1/users"
            }
        }


class SuccessResponse(BaseModel):
    """Standard success response format."""
    success: bool = Field(True, description="Always true for success responses")
    message: Optional[str] = Field(None, description="Success message")
    data: Optional[Any] = Field(None, description="Response data")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {"id": 1, "name": "example"},
                "timestamp": "2024-01-01T00:00:00Z"
            }
        }


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")
    total: int = Field(..., description="Total number of items")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


class PaginatedResponse(BaseModel):
    """Paginated response format."""
    success: bool = Field(True, description="Always true for success responses")
    data: List[Any] = Field(..., description="List of items")
    meta: PaginationMeta = Field(..., description="Pagination metadata")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": [{"id": 1, "name": "item1"}, {"id": 2, "name": "item2"}],
                "meta": {
                    "page": 1,
                    "per_page": 10,
                    "total": 25,
                    "pages": 3,
                    "has_next": True,
                    "has_prev": False
                },
                "timestamp": "2024-01-01T00:00:00Z"
            }
        }


class HealthStatus(str, Enum):
    """Health check status."""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


class ServiceHealth(BaseModel):
    """Individual service health status."""
    name: str = Field(..., description="Service name")
    status: HealthStatus = Field(..., description="Service status")
    response_time_ms: Optional[float] = Field(None, description="Response time in milliseconds")
    error: Optional[str] = Field(None, description="Error message if unhealthy")
    last_check: datetime = Field(default_factory=datetime.utcnow, description="Last health check time")


class HealthResponse(BaseModel):
    """Health check response."""
    success: bool = Field(True, description="Overall health status")
    status: HealthStatus = Field(..., description="Overall system status")
    services: List[ServiceHealth] = Field(..., description="Individual service statuses")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")
    version: Optional[str] = Field(None, description="Application version")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "status": "healthy",
                "services": [
                    {
                        "name": "database",
                        "status": "healthy",
                        "response_time_ms": 15.5,
                        "last_check": "2024-01-01T00:00:00Z"
                    },
                    {
                        "name": "ai_service",
                        "status": "healthy",
                        "response_time_ms": 120.3,
                        "last_check": "2024-01-01T00:00:00Z"
                    }
                ],
                "timestamp": "2024-01-01T00:00:00Z",
                "version": "1.0.0"
            }
        }