"""Tests for shop list_api_v1_shop_summary endpoint."""

from app.main import app
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
import pytest

class TestListApiV1ShopSummary:
    """Test cases for list_api_v1_shop_summary endpoint."""
    
    @pytest.mark.asyncio
    async def test_get_shop_success(self):
        """Test successful get request to /api/v1/shop/summary."""

        
        # Test data
        test_data = {}
        
        # Mock service response
        with patch("app.api.v1.routes_shop.ShopService") as mock_service:
            mock_instance = AsyncMock()
            mock_service.return_value = mock_instance
            
            # Configure mock response
            mock_instance.list_api_v1_shop_summary.return_value = {"message": "success"}
            
            # Make request
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/api/v1/shop/summary")
            
            # Assertions
            assert response.status_code == 200
            response_data = response.json()
            assert isinstance(response_data, dict)


