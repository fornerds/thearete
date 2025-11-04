"""Comprehensive AI service tests."""

import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient

from app.ai.client import (
    AIClient,
    MockAIClient,
    OpenAIClient,
    GenericHTTPClient,
    AIError,
    AITimeoutError,
    AICircuitBreakerError,
    AIRequestError
)


@pytest.fixture
async def mock_ai_client():
    """Create a mock AI client for testing."""
    return MockAIClient()


@pytest.fixture
async def test_user(db):
    """Create a test user."""
    from app.db.models.user import User
    from app.core.security import get_password_hash
    
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        is_active=True,
        is_superuser=False
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


class TestAIClientInterface:
    """Test AI client interface implementations."""
    
    async def test_mock_client_complete(self, mock_ai_client):
        """Test mock client text completion."""
        result = await mock_ai_client.complete("Test prompt")
        
        assert isinstance(result, str)
        assert "Mock completion" in result
        assert "Test prompt" in result
    
    async def test_mock_client_embed(self, mock_ai_client):
        """Test mock client embeddings."""
        texts = ["Hello", "World"]
        embeddings = await mock_ai_client.embed(texts)
        
        assert isinstance(embeddings, list)
        assert len(embeddings) == 2
        assert all(isinstance(emb, list) for emb in embeddings)
        assert all(len(emb) == 3 for emb in embeddings)
    
    async def test_mock_client_chat(self, mock_ai_client):
        """Test mock client chat completion."""
        messages = [{"role": "user", "content": "Hello"}]
        result = await mock_ai_client.chat(messages)
        
        assert isinstance(result, str)
        assert "Mock chat response" in result
        assert "Hello" in result
    
    async def test_mock_client_ping(self, mock_ai_client):
        """Test mock client ping."""
        result = await mock_ai_client.ping()
        assert result is True


class TestAIEndpoints:
    """Test AI API endpoints."""
    
    async def test_complete_text_success(self, client: AsyncClient, test_user):
        """Test successful text completion."""
        # Login to get token
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        login_response = await client.post("/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # Test text completion
        headers = {"Authorization": f"Bearer {access_token}"}
        completion_data = {
            "prompt": "Write a short story about a robot",
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        response = await client.post("/v1/ai/complete", json=completion_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "text" in data
        assert "model" in data
        assert isinstance(data["text"], str)
        assert len(data["text"]) > 0
    
    async def test_complete_text_unauthorized(self, client: AsyncClient):
        """Test text completion without authentication."""
        completion_data = {
            "prompt": "Write a short story about a robot",
            "max_tokens": 100
        }
        
        response = await client.post("/v1/ai/complete", json=completion_data)
        
        assert response.status_code == 401
        data = response.json()
        
        assert data["success"] is False
        assert data["error"] == "UNAUTHORIZED"
    
    async def test_complete_text_invalid_request(self, client: AsyncClient, test_user):
        """Test text completion with invalid request."""
        # Login to get token
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        login_response = await client.post("/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # Test with invalid data
        headers = {"Authorization": f"Bearer {access_token}"}
        completion_data = {
            "prompt": "",  # Empty prompt
            "max_tokens": -1,  # Invalid max_tokens
            "temperature": 3.0  # Invalid temperature
        }
        
        response = await client.post("/v1/ai/complete", json=completion_data, headers=headers)
        
        assert response.status_code == 422
        data = response.json()
        
        assert data["success"] is False
        assert data["error"] == "VALIDATION_ERROR"
    
    async def test_generate_embeddings_success(self, client: AsyncClient, test_user):
        """Test successful embeddings generation."""
        # Login to get token
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        login_response = await client.post("/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # Test embeddings generation
        headers = {"Authorization": f"Bearer {access_token}"}
        embedding_data = {
            "texts": ["Hello world", "AI is amazing"],
            "model": "text-embedding-ada-002"
        }
        
        response = await client.post("/v1/ai/embed", json=embedding_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "embeddings" in data
        assert "model" in data
        assert isinstance(data["embeddings"], list)
        assert len(data["embeddings"]) == 2
        assert all(isinstance(emb, list) for emb in data["embeddings"])
    
    async def test_chat_completion_success(self, client: AsyncClient, test_user):
        """Test successful chat completion."""
        # Login to get token
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        login_response = await client.post("/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # Test chat completion
        headers = {"Authorization": f"Bearer {access_token}"}
        chat_data = {
            "messages": [
                {"role": "user", "content": "What is the capital of France?"}
            ],
            "max_tokens": 50,
            "temperature": 0.7
        }
        
        response = await client.post("/v1/ai/chat", json=chat_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "response" in data
        assert "model" in data
        assert isinstance(data["response"], str)
        assert len(data["response"]) > 0
    
    async def test_ping_ai_service(self, client: AsyncClient):
        """Test AI service ping."""
        response = await client.get("/v1/ai/ping")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "AI service is available" in data["message"]
        assert "status" in data["data"]
    
    async def test_ai_status(self, client: AsyncClient):
        """Test AI service status."""
        response = await client.get("/v1/ai/status")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "AI service status retrieved" in data["message"]
        assert "data" in data
        
        status_data = data["data"]
        assert "available" in status_data
        assert "circuit_breaker_state" in status_data


class TestAIErrorHandling:
    """Test AI error handling scenarios."""
    
    async def test_timeout_error_handling(self, client: AsyncClient, test_user):
        """Test timeout error handling."""
        # Login to get token
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        login_response = await client.post("/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # Mock timeout error
        with patch('app.ai.client.get_ai_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.complete.side_effect = AITimeoutError("Request timeout")
            mock_get_client.return_value = mock_client
            
            headers = {"Authorization": f"Bearer {access_token}"}
            completion_data = {
                "prompt": "Test prompt",
                "max_tokens": 100
            }
            
            response = await client.post("/v1/ai/complete", json=completion_data, headers=headers)
            
            assert response.status_code == 408
            data = response.json()
            
            assert data["success"] is False
            assert "timed out" in data["message"]
    
    async def test_circuit_breaker_error_handling(self, client: AsyncClient, test_user):
        """Test circuit breaker error handling."""
        # Login to get token
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        login_response = await client.post("/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # Mock circuit breaker error
        with patch('app.ai.client.get_ai_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.complete.side_effect = AICircuitBreakerError("Circuit breaker is OPEN")
            mock_get_client.return_value = mock_client
            
            headers = {"Authorization": f"Bearer {access_token}"}
            completion_data = {
                "prompt": "Test prompt",
                "max_tokens": 100
            }
            
            response = await client.post("/v1/ai/complete", json=completion_data, headers=headers)
            
            assert response.status_code == 503
            data = response.json()
            
            assert data["success"] is False
            assert "temporarily unavailable" in data["message"]
    
    async def test_request_error_handling(self, client: AsyncClient, test_user):
        """Test request error handling."""
        # Login to get token
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        login_response = await client.post("/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # Mock request error
        with patch('app.ai.client.get_ai_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.complete.side_effect = AIRequestError("API error 500: Internal server error")
            mock_get_client.return_value = mock_client
            
            headers = {"Authorization": f"Bearer {access_token}"}
            completion_data = {
                "prompt": "Test prompt",
                "max_tokens": 100
            }
            
            response = await client.post("/v1/ai/complete", json=completion_data, headers=headers)
            
            assert response.status_code == 503
            data = response.json()
            
            assert data["success"] is False
            assert "request failed" in data["message"]


class TestAIClientResilience:
    """Test AI client resilience features."""
    
    async def test_circuit_breaker_functionality(self):
        """Test circuit breaker functionality."""
        from app.ai.client import CircuitBreaker
        
        circuit_breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=1)
        
        # Mock function that fails
        async def failing_function():
            raise Exception("Test error")
        
        wrapped_function = circuit_breaker(failing_function)
        
        # First failure
        with pytest.raises(Exception):
            await wrapped_function()
        
        assert circuit_breaker.failure_count == 1
        assert circuit_breaker.state == "CLOSED"
        
        # Second failure - should open circuit breaker
        with pytest.raises(Exception):
            await wrapped_function()
        
        assert circuit_breaker.failure_count == 2
        assert circuit_breaker.state == "OPEN"
        
        # Third call should raise circuit breaker error
        with pytest.raises(AICircuitBreakerError):
            await wrapped_function()
    
    async def test_retry_mechanism(self):
        """Test retry mechanism with tenacity."""
        from app.ai.client import OpenAIClient
        import httpx
        
        # Create client with short timeout for testing
        client = OpenAIClient(
            api_key="test-key",
            base_url="http://localhost:9999",  # Non-existent URL
            timeout=1,
            max_retries=2
        )
        
        # This should trigger retries and eventually fail
        with pytest.raises((AITimeoutError, AIRequestError)):
            await client.complete("Test prompt")
        
        await client.close()
    
    async def test_request_logging(self, caplog):
        """Test request and response logging."""
        mock_client = MockAIClient()
        
        # Test completion with logging
        await mock_client.complete("Test prompt")
        
        # Check that logs were generated
        log_messages = [record.message for record in caplog.records]
        
        # Should have request and response logs
        request_logs = [msg for msg in log_messages if "AI Request" in msg]
        response_logs = [msg for msg in log_messages if "AI Response" in msg]
        
        assert len(request_logs) > 0
        assert len(response_logs) > 0
        
        # Check log format
        assert any("complete" in msg for msg in request_logs)
        assert any("SUCCESS" in msg for msg in response_logs)


class TestAIClientFactory:
    """Test AI client factory functions."""
    
    async def test_create_mock_client(self):
        """Test creating mock AI client."""
        from app.ai.client import create_ai_client, AIProvider
        
        client = create_ai_client(AIProvider.MOCK)
        assert isinstance(client, MockAIClient)
    
    async def test_create_openai_client(self):
        """Test creating OpenAI client."""
        from app.ai.client import create_ai_client, AIProvider
        
        client = create_ai_client(AIProvider.OPENAI)
        assert isinstance(client, OpenAIClient)
        assert client.api_key == ""  # Default empty key
        assert client.base_url == "https://api.openai.com/v1"
    
    async def test_create_generic_client(self):
        """Test creating generic HTTP client."""
        from app.ai.client import create_ai_client, AIProvider
        
        client = create_ai_client(AIProvider.GENERIC)
        assert isinstance(client, GenericHTTPClient)
        assert client.base_url == "https://api.openai.com/v1"
    
    async def test_global_client_management(self):
        """Test global AI client management."""
        from app.ai.client import get_ai_client, set_ai_client, close_ai_client
        
        # Test getting default client
        client1 = await get_ai_client()
        assert isinstance(client1, MockAIClient)
        
        # Test setting custom client
        custom_client = MockAIClient()
        set_ai_client(custom_client)
        
        client2 = await get_ai_client()
        assert client2 is custom_client
        
        # Test closing client
        await close_ai_client()
        client3 = await get_ai_client()
        assert client3 is not custom_client  # Should create new instance
