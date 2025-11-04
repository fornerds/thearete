"""AI service routes for text completion and embeddings."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.ai.client import (
    get_ai_client,
    AIClient,
    AIError,
    AITimeoutError,
    AICircuitBreakerError,
    AIRequestError
)
from app.core.auth import get_current_user
from app.core.exceptions import BaseAPIException
from app.db.models.user import User
from app.schemas.common import ErrorCode, ErrorResponse, SuccessResponse

router = APIRouter(prefix="/ai", tags=["AI"])


class CompletionRequest(BaseModel):
    """Text completion request schema."""
    prompt: str = Field(..., min_length=1, max_length=10000, description="Text prompt for completion")
    max_tokens: Optional[int] = Field(None, ge=1, le=4000, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="Sampling temperature")
    model: Optional[str] = Field(None, description="Model to use for completion")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Write a short story about a robot learning to paint",
                "max_tokens": 500,
                "temperature": 0.7,
                "model": "gpt-3.5-turbo"
            }
        }


class CompletionResponse(BaseModel):
    """Text completion response schema."""
    text: str = Field(..., description="Generated text completion")
    model: str = Field(..., description="Model used for completion")
    usage: Optional[dict] = Field(None, description="Token usage information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Once upon a time, there was a robot named ARIA who discovered the joy of painting...",
                "model": "gpt-3.5-turbo",
                "usage": {"prompt_tokens": 15, "completion_tokens": 150, "total_tokens": 165}
            }
        }


class EmbeddingRequest(BaseModel):
    """Embedding request schema."""
    texts: List[str] = Field(..., min_items=1, max_items=100, description="Texts to embed")
    model: Optional[str] = Field(None, description="Model to use for embeddings")
    
    class Config:
        json_schema_extra = {
            "example": {
                "texts": ["Hello world", "AI is amazing"],
                "model": "text-embedding-ada-002"
            }
        }


class EmbeddingResponse(BaseModel):
    """Embedding response schema."""
    embeddings: List[List[float]] = Field(..., description="Generated embeddings")
    model: str = Field(..., description="Model used for embeddings")
    usage: Optional[dict] = Field(None, description="Token usage information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "embeddings": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
                "model": "text-embedding-ada-002",
                "usage": {"prompt_tokens": 10, "total_tokens": 10}
            }
        }


class ChatRequest(BaseModel):
    """Chat completion request schema."""
    messages: List[dict] = Field(..., min_items=1, description="Chat messages")
    max_tokens: Optional[int] = Field(None, ge=1, le=4000, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="Sampling temperature")
    model: Optional[str] = Field(None, description="Model to use for chat")
    
    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {"role": "user", "content": "What is the capital of France?"}
                ],
                "max_tokens": 100,
                "temperature": 0.7,
                "model": "gpt-3.5-turbo"
            }
        }


class ChatResponse(BaseModel):
    """Chat completion response schema."""
    response: str = Field(..., description="Chat response")
    model: str = Field(..., description="Model used for chat")
    usage: Optional[dict] = Field(None, description="Token usage information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "The capital of France is Paris.",
                "model": "gpt-3.5-turbo",
                "usage": {"prompt_tokens": 10, "completion_tokens": 8, "total_tokens": 18}
            }
        }


@router.post(
    "/complete",
    response_model=CompletionResponse,
    summary="Text Completion",
    description="Generate text completion from a prompt using AI",
    responses={
        200: {"description": "Text completion generated successfully"},
        400: {"description": "Invalid request"},
        401: {"description": "Unauthorized"},
        408: {"description": "Request timeout"},
        503: {"description": "AI service unavailable"}
    }
)
async def complete_text(
    request: CompletionRequest,
    current_user: User = Depends(get_current_user),
    ai_client: AIClient = Depends(get_ai_client)
) -> CompletionResponse:
    """Generate text completion from a prompt."""
    try:
        text = await ai_client.complete(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            model=request.model
        )
        
        return CompletionResponse(
            text=text,
            model=request.model or "default",
            usage=None  # Usage info would come from the AI client response
        )
        
    except AITimeoutError as e:
        raise BaseAPIException(
            message="AI request timed out. Please try again.",
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=status.HTTP_408_REQUEST_TIMEOUT
        )
    except AICircuitBreakerError as e:
        raise BaseAPIException(
            message="AI service is temporarily unavailable. Please try again later.",
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except AIRequestError as e:
        raise BaseAPIException(
            message=f"AI request failed: {str(e)}",
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except AIError as e:
        raise BaseAPIException(
            message=f"AI service error: {str(e)}",
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


@router.post(
    "/embed",
    response_model=EmbeddingResponse,
    summary="Generate Embeddings",
    description="Generate embeddings for input texts using AI",
    responses={
        200: {"description": "Embeddings generated successfully"},
        400: {"description": "Invalid request"},
        401: {"description": "Unauthorized"},
        408: {"description": "Request timeout"},
        503: {"description": "AI service unavailable"}
    }
)
async def generate_embeddings(
    request: EmbeddingRequest,
    current_user: User = Depends(get_current_user),
    ai_client: AIClient = Depends(get_ai_client)
) -> EmbeddingResponse:
    """Generate embeddings for input texts."""
    try:
        embeddings = await ai_client.embed(
            texts=request.texts,
            model=request.model
        )
        
        return EmbeddingResponse(
            embeddings=embeddings,
            model=request.model or "default",
            usage=None  # Usage info would come from the AI client response
        )
        
    except AITimeoutError as e:
        raise BaseAPIException(
            message="AI embeddings request timed out. Please try again.",
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=status.HTTP_408_REQUEST_TIMEOUT
        )
    except AICircuitBreakerError as e:
        raise BaseAPIException(
            message="AI service is temporarily unavailable. Please try again later.",
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except AIRequestError as e:
        raise BaseAPIException(
            message=f"AI embeddings request failed: {str(e)}",
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except AIError as e:
        raise BaseAPIException(
            message=f"AI service error: {str(e)}",
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat Completion",
    description="Generate chat completion from messages using AI",
    responses={
        200: {"description": "Chat completion generated successfully"},
        400: {"description": "Invalid request"},
        401: {"description": "Unauthorized"},
        408: {"description": "Request timeout"},
        503: {"description": "AI service unavailable"}
    }
)
async def chat_completion(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    ai_client: AIClient = Depends(get_ai_client)
) -> ChatResponse:
    """Generate chat completion from messages."""
    try:
        response = await ai_client.chat(
            messages=request.messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            model=request.model
        )
        
        return ChatResponse(
            response=response,
            model=request.model or "default",
            usage=None  # Usage info would come from the AI client response
        )
        
    except AITimeoutError as e:
        raise BaseAPIException(
            message="AI chat request timed out. Please try again.",
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=status.HTTP_408_REQUEST_TIMEOUT
        )
    except AICircuitBreakerError as e:
        raise BaseAPIException(
            message="AI service is temporarily unavailable. Please try again later.",
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except AIRequestError as e:
        raise BaseAPIException(
            message=f"AI chat request failed: {str(e)}",
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except AIError as e:
        raise BaseAPIException(
            message=f"AI service error: {str(e)}",
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


@router.get(
    "/ping",
    summary="AI Service Ping",
    description="Check AI service connectivity",
    responses={
        200: {"description": "AI service is available"},
        503: {"description": "AI service is unavailable"}
    }
)
async def ping_ai_service(
    ai_client: AIClient = Depends(get_ai_client)
) -> SuccessResponse:
    """Ping AI service to check connectivity."""
    try:
        is_available = await ai_client.ping()
        
        if is_available:
            return SuccessResponse(
                message="AI service is available",
                data={"status": "healthy"}
            )
        else:
            raise BaseAPIException(
                message="AI service is not responding",
                error_code=ErrorCode.INTERNAL_ERROR,
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE
            )
            
    except Exception as e:
        raise BaseAPIException(
            message=f"AI service ping failed: {str(e)}",
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


@router.get(
    "/status",
    summary="AI Service Status",
    description="Get detailed AI service status information",
    responses={
        200: {"description": "AI service status retrieved successfully"},
        503: {"description": "AI service is unavailable"}
    }
)
async def get_ai_status(
    ai_client: AIClient = Depends(get_ai_client)
) -> SuccessResponse:
    """Get detailed AI service status."""
    try:
        # Test ping
        is_available = await ai_client.ping()
        
        # Get circuit breaker status
        circuit_breaker_status = "unknown"
        if hasattr(ai_client, 'circuit_breaker'):
            circuit_breaker_status = ai_client.circuit_breaker.state
        
        status_data = {
            "available": is_available,
            "circuit_breaker_state": circuit_breaker_status,
            "timeout": getattr(ai_client, 'timeout', 'unknown'),
            "max_retries": getattr(ai_client, 'max_retries', 'unknown')
        }
        
        return SuccessResponse(
            message="AI service status retrieved",
            data=status_data
        )
        
    except Exception as e:
        raise BaseAPIException(
            message=f"Failed to get AI service status: {str(e)}",
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
