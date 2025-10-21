"""AI client interface for external model integration."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class AIClient(ABC):
    """Abstract base class for AI client implementations."""
    
    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any
    ) -> str:
        """Generate text from a prompt."""
        pass
    
    @abstractmethod
    async def generate_embeddings(
        self,
        texts: List[str],
        **kwargs: Any
    ) -> List[List[float]]:
        """Generate embeddings for texts."""
        pass
    
    @abstractmethod
    async def chat_completion(
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


class MockAIClient(AIClient):
    """Mock AI client for development and testing."""
    
    async def generate_text(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any
    ) -> str:
        """Generate mock text."""
        return f"Mock response to: {prompt[:50]}..."
    
    async def generate_embeddings(
        self,
        texts: List[str],
        **kwargs: Any
    ) -> List[List[float]]:
        """Generate mock embeddings."""
        return [[0.1, 0.2, 0.3] for _ in texts]
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any
    ) -> str:
        """Generate mock chat completion."""
        last_message = messages[-1]["content"] if messages else "Hello"
        return f"Mock chat response to: {last_message[:50]}..."
    
    async def ping(self) -> bool:
        """Mock ping - always returns True."""
        return True


# Global AI client instance
ai_client: AIClient = MockAIClient()


def get_ai_client() -> AIClient:
    """Get the global AI client instance."""
    return ai_client


def set_ai_client(client: AIClient) -> None:
    """Set the global AI client instance."""
    global ai_client
    ai_client = client
