"""Custom exceptions and exception handlers."""

import logging
from datetime import datetime
from typing import Union

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app.schemas.common import ErrorCode, ErrorResponse, ErrorDetail

logger = logging.getLogger(__name__)


class BaseAPIException(Exception):
    """Base exception for API errors."""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.INTERNAL_ERROR,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: list[ErrorDetail] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or []
        super().__init__(self.message)


class ValidationException(BaseAPIException):
    """Validation error exception."""
    
    def __init__(self, message: str = "Validation failed", details: list[ErrorDetail] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.VALIDATION_ERROR,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details or []
        )


class IntegrityException(BaseAPIException):
    """Database integrity error exception."""
    
    def __init__(self, message: str = "Database integrity error", details: list[ErrorDetail] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.INTEGRITY_ERROR,
            status_code=status.HTTP_409_CONFLICT,
            details=details or []
        )


class ConflictException(BaseAPIException):
    """Conflict exception for resource conflicts."""
    
    def __init__(self, message: str = "Resource conflict", details: list[ErrorDetail] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.INTEGRITY_ERROR,
            status_code=status.HTTP_409_CONFLICT,
            details=details or []
        )


class NotFoundException(BaseAPIException):
    """Resource not found exception."""
    
    def __init__(self, message: str = "Resource not found", details: list[ErrorDetail] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details or []
        )


class UnauthorizedException(BaseAPIException):
    """Unauthorized access exception."""
    
    def __init__(self, message: str = "Unauthorized access", details: list[ErrorDetail] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.UNAUTHORIZED,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details or []
        )


class ForbiddenException(BaseAPIException):
    """Forbidden access exception."""
    
    def __init__(self, message: str = "Forbidden access", details: list[ErrorDetail] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.FORBIDDEN,
            status_code=status.HTTP_403_FORBIDDEN,
            details=details or []
        )


class TokenExpiredException(BaseAPIException):
    """Token expired exception."""
    
    def __init__(self, message: str = "Token has expired", details: list[ErrorDetail] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.TOKEN_EXPIRED,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details or []
        )


class TokenInvalidException(BaseAPIException):
    """Invalid token exception."""
    
    def __init__(self, message: str = "Invalid token", details: list[ErrorDetail] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.TOKEN_INVALID,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details or []
        )


class UserInactiveException(BaseAPIException):
    """Inactive user exception."""
    
    def __init__(self, message: str = "User account is inactive", details: list[ErrorDetail] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.USER_INACTIVE,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details or []
        )


class InvalidCredentialsException(BaseAPIException):
    """Invalid credentials exception."""
    
    def __init__(self, message: str = "Invalid credentials", details: list[ErrorDetail] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.INVALID_CREDENTIALS,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details or []
        )


def create_error_response(
    error_code: ErrorCode,
    message: str,
    status_code: int,
    details: list[ErrorDetail] = None,
    path: str = None
) -> JSONResponse:
    """Create standardized error response."""
    error_response = ErrorResponse(
        error=error_code,
        message=message,
        details=details or [],
        path=path
    )
    
    # Use model_dump with mode='json' to properly serialize datetime
    try:
        content = error_response.model_dump(mode='json')
    except AttributeError:
        # Fallback for older Pydantic versions
        content = error_response.model_dump()
        # Convert datetime objects to ISO format strings
        import json
        content = json.loads(json.dumps(content, default=str))
    
    return JSONResponse(
        status_code=status_code,
        content=content
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers with the FastAPI app."""
    
    @app.exception_handler(BaseAPIException)
    async def base_api_exception_handler(request: Request, exc: BaseAPIException):
        """Handle custom API exceptions."""
        logger.warning(f"API Exception: {exc.error_code} - {exc.message} at {request.url}")
        
        return create_error_response(
            error_code=exc.error_code,
            message=exc.message,
            status_code=exc.status_code,
            details=exc.details,
            path=str(request.url.path)
        )
    
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        """Handle Pydantic validation errors."""
        logger.warning(f"Validation Error: {exc.errors()} at {request.url}")
        
        details = []
        for error in exc.errors():
            details.append(ErrorDetail(
                field=".".join(str(loc) for loc in error["loc"]) if error["loc"] else None,
                message=error["msg"],
                code=error["type"]
            ))
        
        return create_error_response(
            error_code=ErrorCode.VALIDATION_ERROR,
            message="Validation failed",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details,
            path=str(request.url.path)
        )
    
    @app.exception_handler(IntegrityError)
    async def integrity_exception_handler(request: Request, exc: IntegrityError):
        """Handle database integrity errors."""
        logger.error(f"Integrity Error: {str(exc)} at {request.url}")
        
        # Extract meaningful error message
        error_msg = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
        if "UNIQUE constraint failed" in error_msg:
            message = "Resource already exists"
        elif "FOREIGN KEY constraint failed" in error_msg:
            message = "Referenced resource not found"
        else:
            message = "Database integrity error"
        
        return create_error_response(
            error_code=ErrorCode.INTEGRITY_ERROR,
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            path=str(request.url.path)
        )
    
    @app.exception_handler(NoResultFound)
    async def no_result_found_handler(request: Request, exc: NoResultFound):
        """Handle SQLAlchemy NoResultFound exceptions."""
        logger.warning(f"Resource not found: {str(exc)} at {request.url}")
        
        return create_error_response(
            error_code=ErrorCode.NOT_FOUND,
            message="Resource not found",
            status_code=status.HTTP_404_NOT_FOUND,
            path=str(request.url.path)
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle FastAPI HTTP exceptions."""
        logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail} at {request.url}")
        
        # Map HTTP status codes to error codes
        error_code_mapping = {
            status.HTTP_400_BAD_REQUEST: ErrorCode.VALIDATION_ERROR,
            status.HTTP_401_UNAUTHORIZED: ErrorCode.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: ErrorCode.FORBIDDEN,
            status.HTTP_404_NOT_FOUND: ErrorCode.NOT_FOUND,
            status.HTTP_409_CONFLICT: ErrorCode.INTEGRITY_ERROR,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ErrorCode.VALIDATION_ERROR,
        }
        
        error_code = error_code_mapping.get(exc.status_code, ErrorCode.INTERNAL_ERROR)
        
        return create_error_response(
            error_code=error_code,
            message=str(exc.detail),
            status_code=exc.status_code,
            path=str(request.url.path)
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all other exceptions."""
        logger.error(f"Unhandled Exception: {type(exc).__name__}: {str(exc)} at {request.url}", exc_info=True)
        
        return create_error_response(
            error_code=ErrorCode.INTERNAL_ERROR,
            message="Internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            path=str(request.url.path)
        )