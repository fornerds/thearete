"""Resilient AI client interface for external model integration."""

import asyncio
import logging
import time
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from enum import Enum

import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    after_log
)

from app.config import settings

logger = logging.getLogger(__name__)


class AIProvider(str, Enum):
    """Supported AI providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GENERIC = "generic"
    MOCK = "mock"


class AIError(Exception):
    """Base AI client error."""
    pass


class AITimeoutError(AIError):
    """AI request timeout error."""
    pass


class AICircuitBreakerError(AIError):
    """AI circuit breaker error."""
    pass


class AIRequestError(AIError):
    """AI request error."""
    pass


class CircuitBreaker:
    """Simple circuit breaker implementation."""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def __call__(self, func):
        async def wrapper(*args, **kwargs):
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = "HALF_OPEN"
                else:
                    raise AICircuitBreakerError("Circuit breaker is OPEN")
            
            try:
                result = await func(*args, **kwargs)
                if self.state == "HALF_OPEN":
                    self.state = "CLOSED"
                    self.failure_count = 0
                return result
            except self.expected_exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                
                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
                    logger.warning(f"Circuit breaker opened after {self.failure_count} failures")
                
                raise e
        
        return wrapper


class AIClient(ABC):
    """Abstract base class for AI client implementations."""
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.circuit_breaker = CircuitBreaker()
    
    @abstractmethod
    async def complete(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any
    ) -> str:
        """Complete text from a prompt."""
        pass
    
    @abstractmethod
    async def embed(
        self,
        texts: List[str],
        **kwargs: Any
    ) -> List[List[float]]:
        """Generate embeddings for texts."""
        pass
    
    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any
    ) -> str:
        """Generate chat completion."""
        pass
    
    @abstractmethod
    async def ping(self) -> bool:
        """Ping the AI service to check connectivity."""
        pass
    
    def _generate_request_id(self) -> str:
        """Generate unique request ID."""
        return str(uuid.uuid4())[:8]
    
    def _log_request(self, request_id: str, method: str, **kwargs):
        """Log AI request."""
        logger.info(f"AI Request [{request_id}] {method}: {kwargs}")
    
    def _log_response(self, request_id: str, method: str, duration: float, success: bool):
        """Log AI response."""
        status = "SUCCESS" if success else "FAILED"
        logger.info(f"AI Response [{request_id}] {method}: {status} ({duration:.2f}s)")


class OpenAIClient(AIClient):
    """OpenAI API client with resilience features."""
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.openai.com/v1",
        timeout: int = 30,
        max_retries: int = 3
    ):
        super().__init__(timeout, max_retries)
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        after=after_log(logger, logging.INFO)
    )
    async def complete(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any
    ) -> str:
        """Complete text using OpenAI API."""
        request_id = self._generate_request_id()
        start_time = time.time()
        
        self._log_request(request_id, "complete", prompt_length=len(prompt))
        
        try:
            payload = {
                "model": kwargs.get("model", "gpt-3.5-turbo"),
                "prompt": prompt,
                "max_tokens": max_tokens or 1000,
                "temperature": temperature or 0.7,
                **kwargs
            }
            
            response = await self.client.post(
                f"{self.base_url}/completions",
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            result = data["choices"][0]["text"].strip()
            
            duration = time.time() - start_time
            self._log_response(request_id, "complete", duration, True)
            
            return result
            
        except httpx.TimeoutException as e:
            duration = time.time() - start_time
            self._log_response(request_id, "complete", duration, False)
            raise AITimeoutError(f"OpenAI request timeout: {e}")
        except httpx.HTTPStatusError as e:
            duration = time.time() - start_time
            self._log_response(request_id, "complete", duration, False)
            raise AIRequestError(f"OpenAI API error {e.response.status_code}: {e.response.text}")
        except Exception as e:
            duration = time.time() - start_time
            self._log_response(request_id, "complete", duration, False)
            raise AIRequestError(f"OpenAI request failed: {e}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        after=after_log(logger, logging.INFO)
    )
    async def embed(
        self,
        texts: List[str],
        **kwargs: Any
    ) -> List[List[float]]:
        """Generate embeddings using OpenAI API."""
        request_id = self._generate_request_id()
        start_time = time.time()
        
        self._log_request(request_id, "embed", text_count=len(texts))
        
        try:
            payload = {
                "model": kwargs.get("model", "text-embedding-ada-002"),
                "input": texts,
                **kwargs
            }
            
            response = await self.client.post(
                f"{self.base_url}/embeddings",
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            embeddings = [item["embedding"] for item in data["data"]]
            
            duration = time.time() - start_time
            self._log_response(request_id, "embed", duration, True)
            
            return embeddings
            
        except httpx.TimeoutException as e:
            duration = time.time() - start_time
            self._log_response(request_id, "embed", duration, False)
            raise AITimeoutError(f"OpenAI embeddings timeout: {e}")
        except httpx.HTTPStatusError as e:
            duration = time.time() - start_time
            self._log_response(request_id, "embed", duration, False)
            raise AIRequestError(f"OpenAI embeddings error {e.response.status_code}: {e.response.text}")
        except Exception as e:
            duration = time.time() - start_time
            self._log_response(request_id, "embed", duration, False)
            raise AIRequestError(f"OpenAI embeddings failed: {e}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        after=after_log(logger, logging.INFO)
    )
    async def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any
    ) -> str:
        """Generate chat completion using OpenAI API."""
        request_id = self._generate_request_id()
        start_time = time.time()
        
        self._log_request(request_id, "chat", message_count=len(messages))
        
        try:
            payload = {
                "model": kwargs.get("model", "gpt-3.5-turbo"),
                "messages": messages,
                "max_tokens": max_tokens or 1000,
                "temperature": temperature or 0.7,
                **kwargs
            }
            
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            result = data["choices"][0]["message"]["content"].strip()
            
            duration = time.time() - start_time
            self._log_response(request_id, "chat", duration, True)
            
            return result
            
        except httpx.TimeoutException as e:
            duration = time.time() - start_time
            self._log_response(request_id, "chat", duration, False)
            raise AITimeoutError(f"OpenAI chat timeout: {e}")
        except httpx.HTTPStatusError as e:
            duration = time.time() - start_time
            self._log_response(request_id, "chat", duration, False)
            raise AIRequestError(f"OpenAI chat error {e.response.status_code}: {e.response.text}")
        except Exception as e:
            duration = time.time() - start_time
            self._log_response(request_id, "chat", duration, False)
            raise AIRequestError(f"OpenAI chat failed: {e}")
    
    async def ping(self) -> bool:
        """Ping OpenAI API."""
        try:
            response = await self.client.get(f"{self.base_url}/models", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"OpenAI ping failed: {e}")
            return False
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


class GenericHTTPClient(AIClient):
    """Generic HTTP client for any AI API."""
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(timeout, max_retries)
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        
        default_headers = {"Content-Type": "application/json"}
        if api_key:
            default_headers["Authorization"] = f"Bearer {api_key}"
        if headers:
            default_headers.update(headers)
        
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            headers=default_headers
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        after=after_log(logger, logging.INFO)
    )
    async def complete(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any
    ) -> str:
        """Complete text using generic HTTP API."""
        request_id = self._generate_request_id()
        start_time = time.time()
        
        self._log_request(request_id, "complete", prompt_length=len(prompt))
        
        try:
            payload = {
                "prompt": prompt,
                "max_tokens": max_tokens or 1000,
                "temperature": temperature or 0.7,
                **kwargs
            }
            
            response = await self.client.post(
                f"{self.base_url}/complete",
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            result = data.get("text", data.get("response", "")).strip()
            
            duration = time.time() - start_time
            self._log_response(request_id, "complete", duration, True)
            
            return result
            
        except httpx.TimeoutException as e:
            duration = time.time() - start_time
            self._log_response(request_id, "complete", duration, False)
            raise AITimeoutError(f"Generic API timeout: {e}")
        except httpx.HTTPStatusError as e:
            duration = time.time() - start_time
            self._log_response(request_id, "complete", duration, False)
            raise AIRequestError(f"Generic API error {e.response.status_code}: {e.response.text}")
        except Exception as e:
            duration = time.time() - start_time
            self._log_response(request_id, "complete", duration, False)
            raise AIRequestError(f"Generic API request failed: {e}")
    
    async def embed(
        self,
        texts: List[str],
        **kwargs: Any
    ) -> List[List[float]]:
        """Generate embeddings using generic HTTP API."""
        request_id = self._generate_request_id()
        start_time = time.time()
        
        self._log_request(request_id, "embed", text_count=len(texts))
        
        try:
            payload = {
                "texts": texts,
                **kwargs
            }
            
            response = await self.client.post(
                f"{self.base_url}/embeddings",
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            embeddings = data.get("embeddings", [])
            
            duration = time.time() - start_time
            self._log_response(request_id, "embed", duration, True)
            
            return embeddings
            
        except httpx.TimeoutException as e:
            duration = time.time() - start_time
            self._log_response(request_id, "embed", duration, False)
            raise AITimeoutError(f"Generic embeddings timeout: {e}")
        except Exception as e:
            duration = time.time() - start_time
            self._log_response(request_id, "embed", duration, False)
            raise AIRequestError(f"Generic embeddings failed: {e}")
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any
    ) -> str:
        """Generate chat completion using generic HTTP API."""
        request_id = self._generate_request_id()
        start_time = time.time()
        
        self._log_request(request_id, "chat", message_count=len(messages))
        
        try:
            payload = {
                "messages": messages,
                "max_tokens": max_tokens or 1000,
                "temperature": temperature or 0.7,
                **kwargs
            }
            
            response = await self.client.post(
                f"{self.base_url}/chat",
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            result = data.get("response", data.get("text", "")).strip()
            
            duration = time.time() - start_time
            self._log_response(request_id, "chat", duration, True)
            
            return result
            
        except httpx.TimeoutException as e:
            duration = time.time() - start_time
            self._log_response(request_id, "chat", duration, False)
            raise AITimeoutError(f"Generic chat timeout: {e}")
        except Exception as e:
            duration = time.time() - start_time
            self._log_response(request_id, "chat", duration, False)
            raise AIRequestError(f"Generic chat failed: {e}")
    
    async def ping(self) -> bool:
        """Ping generic API."""
        try:
            response = await self.client.get(f"{self.base_url}/ping", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Generic API ping failed: {e}")
            return False
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


class MockAIClient(AIClient):
    """Mock AI client for development and testing."""
    
    def __init__(self, timeout: int = 1, max_retries: int = 1):
        super().__init__(timeout, max_retries)
    
    async def complete(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any
    ) -> str:
        """Generate mock text completion."""
        await asyncio.sleep(0.1)  # Simulate network delay
        return f"Mock completion for: {prompt[:50]}..."
    
    async def embed(
        self,
        texts: List[str],
        **kwargs: Any
    ) -> List[List[float]]:
        """Generate mock embeddings."""
        await asyncio.sleep(0.1)  # Simulate network delay
        return [[0.1, 0.2, 0.3] for _ in texts]
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any
    ) -> str:
        """Generate mock chat completion."""
        await asyncio.sleep(0.1)  # Simulate network delay
        last_message = messages[-1]["content"] if messages else "Hello"
        return f"Mock chat response to: {last_message[:50]}..."
    
    async def ping(self) -> bool:
        """Mock ping - always returns True."""
        await asyncio.sleep(0.05)  # Simulate network delay
        return True


def create_ai_client(provider: AIProvider = None) -> AIClient:
    """Create AI client based on provider."""
    provider = provider or AIProvider(settings.ai_provider)
    
    if provider == AIProvider.OPENAI:
        return OpenAIClient(
            api_key=settings.ai_api_key,
            base_url=settings.ai_base_url,
            timeout=settings.ai_timeout_sec
        )
    elif provider == AIProvider.GENERIC:
        return GenericHTTPClient(
            base_url=settings.ai_base_url,
            api_key=settings.ai_api_key,
            timeout=settings.ai_timeout_sec
        )
    elif provider == AIProvider.MOCK:
        return MockAIClient()
    else:
        raise ValueError(f"Unsupported AI provider: {provider}")


# Global AI client instance
ai_client: Optional[AIClient] = None


async def get_ai_client() -> AIClient:
    """Get the global AI client instance."""
    global ai_client
    if ai_client is None:
        ai_client = create_ai_client()
    return ai_client


def set_ai_client(client: AIClient) -> None:
    """Set the global AI client instance."""
    global ai_client
    ai_client = client


async def close_ai_client():
    """Close the global AI client."""
    global ai_client
    if ai_client and hasattr(ai_client, 'close'):
        await ai_client.close()
    ai_client = None
