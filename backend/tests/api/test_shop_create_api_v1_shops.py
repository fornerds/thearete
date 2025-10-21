"""Tests for shop create_api_v1_shops endpoint."""

from app.main import app
from app.schemas import *
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
import pytest

class TestCreateApiV1Shops:
    """Test cases for create_api_v1_shops endpoint."""
    
    @pytest.mark.asyncio
    async def test_post_shop_success(self):
        """Test successful post request to /api/v1/shops."""

        
        # Test data
        test_data = {'name': '"test_string"', 'address': '"test_string"', 'owner': '"test_string"', 'phone': '"test_string"', 'email': '"test_string"', 'password': '"test_string"'}
        
        # Mock service response
        with patch("app.api.v1.routes_shop.ShopService") as mock_service:
            mock_instance = AsyncMock()
            mock_service.return_value = mock_instance
            
            # Configure mock response
            mock_instance.create_api_v1_shops.return_value = {'shop_id': '"test_string"', 'created_at': '"test_string"'}
            
            # Make request
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/api/v1/shops")
            
            # Assertions
            assert response.status_code == 200
            response_data = response.json()
            assert isinstance(response_data, dict)
            # Add specific field assertions based on response schema

    @pytest.mark.asyncio
    async def test_post_shop_invalid_data(self):
        """Test 422 error with invalid request data."""
        invalid_data = {"invalid_field": "invalid_value"}
        
        # Make request
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/v1/shops", json=invalid_data)
        
        # Assertions
        assert response.status_code == 422


