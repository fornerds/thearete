"""Tests for shop get_api_v1_shops_by_id endpoint."""

from app.main import app
from app.schemas import *
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
import pytest

class TestGetApiV1ShopsById:
    """Test cases for get_api_v1_shops_by_id endpoint."""
    
    @pytest.mark.asyncio
    async def test_get_shop_success(self):
        """Test successful get request to /api/v1/shops/{id}."""

        
        # Test data
        test_data = {}
        
        # Mock service response
        with patch("app.api.v1.routes_shop.ShopService") as mock_service:
            mock_instance = AsyncMock()
            mock_service.return_value = mock_instance
            
            # Configure mock response
            mock_instance.get_api_v1_shops_by_id.return_value = {'shop_id': '"test_string"', 'name': '"test_string"', 'address': '"test_string"', 'owner': '"test_string"'}
            
            # Make request
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/api/v1/shops/{id}")
            
            # Assertions
            assert response.status_code == 200
            response_data = response.json()
            assert isinstance(response_data, dict)
            # Add specific field assertions based on response schema

    @pytest.mark.asyncio
    async def test_get_shop_not_found(self):
        """Test 404 error when shop not found."""
        # Mock service to return None
        with patch("app.api.v1.routes_shop.ShopService") as mock_service:
            mock_instance = AsyncMock()
            mock_service.return_value = mock_instance
            mock_instance.get_api_v1_shops_by_id.return_value = None
            
            # Make request
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/api/v1/shops/{id}")
            
            # Assertions
            assert response.status_code == 404
            assert "not found" in response.json()["detail"].lower()


