"""Comprehensive authentication flow tests."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.db.models.user import User
from app.core.security import get_password_hash


@pytest.fixture
async def test_user(db: AsyncSession) -> User:
    """Create a test user."""
    from app.db.models.user import User
    
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


@pytest.fixture
async def admin_user(db: AsyncSession) -> User:
    """Create an admin test user."""
    from app.db.models.user import User
    
    user = User(
        email="admin@example.com",
        username="admin",
        hashed_password=get_password_hash("adminpassword"),
        full_name="Admin User",
        is_active=True,
        is_superuser=True
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


class TestAuthenticationFlow:
    """Test complete authentication flow."""
    
    async def test_login_success(self, client: AsyncClient, test_user: User):
        """Test successful login."""
        login_data = {
            "email": "test@example.com",
            "password": "testpassword",
            "device_info": "Test Device"
        }
        
        response = await client.post("/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
        assert "refresh_expires_in" in data
        
        # Verify tokens are stored in database
        from app.db.models.token import UserToken
        from sqlalchemy import select
        
        # This would require access to the database session in the test
        # For now, we'll just verify the response structure
    
    async def test_login_invalid_credentials(self, client: AsyncClient):
        """Test login with invalid credentials."""
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        
        response = await client.post("/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        data = response.json()
        
        assert data["success"] is False
        assert data["error"] == "INVALID_CREDENTIALS"
        assert "Invalid email or password" in data["message"]
    
    async def test_login_inactive_user(self, client: AsyncClient, db: AsyncSession):
        """Test login with inactive user."""
        from app.db.models.user import User
        
        user = User(
            email="inactive@example.com",
            username="inactive",
            hashed_password=get_password_hash("password"),
            is_active=False
        )
        
        db.add(user)
        await db.commit()
        
        login_data = {
            "email": "inactive@example.com",
            "password": "password"
        }
        
        response = await client.post("/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        data = response.json()
        
        assert data["success"] is False
        assert data["error"] == "USER_INACTIVE"
    
    async def test_refresh_token_success(self, client: AsyncClient, test_user: User):
        """Test successful token refresh."""
        # First login to get tokens
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        login_response = await client.post("/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        login_data = login_response.json()
        refresh_token = login_data["refresh_token"]
        
        # Use refresh token
        refresh_data = {"refresh_token": refresh_token}
        response = await client.post("/v1/auth/refresh", json=refresh_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    async def test_refresh_token_invalid(self, client: AsyncClient):
        """Test refresh with invalid token."""
        refresh_data = {"refresh_token": "invalid_token"}
        
        response = await client.post("/v1/auth/refresh", json=refresh_data)
        
        assert response.status_code == 401
        data = response.json()
        
        assert data["success"] is False
        assert data["error"] == "TOKEN_INVALID"
    
    async def test_protected_endpoint_access(self, client: AsyncClient, test_user: User):
        """Test accessing protected endpoint with valid token."""
        # Login to get token
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        login_response = await client.post("/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # Access protected endpoint
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get("/v1/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert data["is_active"] is True
    
    async def test_protected_endpoint_no_token(self, client: AsyncClient):
        """Test accessing protected endpoint without token."""
        response = await client.get("/v1/auth/me")
        
        assert response.status_code == 401
        data = response.json()
        
        assert data["success"] is False
        assert data["error"] == "UNAUTHORIZED"
    
    async def test_logout_success(self, client: AsyncClient, test_user: User):
        """Test successful logout."""
        # Login to get tokens
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        login_response = await client.post("/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token_data = login_response.json()
        access_token = token_data["access_token"]
        refresh_token = token_data["refresh_token"]
        
        # Logout
        headers = {"Authorization": f"Bearer {access_token}"}
        logout_data = {"refresh_token": refresh_token}
        
        response = await client.post("/v1/auth/logout", json=logout_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "Session has been revoked" in data["message"]
    
    async def test_logout_revoke_all(self, client: AsyncClient, test_user: User):
        """Test logout with revoke all sessions."""
        # Login to get tokens
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        login_response = await client.post("/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # Logout with revoke all
        headers = {"Authorization": f"Bearer {access_token}"}
        logout_data = {"revoke_all": True}
        
        response = await client.post("/v1/auth/logout", json=logout_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "All sessions have been revoked" in data["message"]
    
    async def test_user_sessions(self, client: AsyncClient, test_user: User):
        """Test getting user sessions."""
        # Login to create session
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        login_response = await client.post("/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # Get sessions
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get("/v1/auth/sessions", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "active_sessions" in data
        assert "sessions" in data
        assert isinstance(data["sessions"], list)
    
    async def test_admin_scope_access(self, client: AsyncClient, admin_user: User):
        """Test admin scope access."""
        # Login as admin
        login_data = {
            "email": "admin@example.com",
            "password": "adminpassword"
        }
        
        login_response = await client.post("/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # Access admin endpoint (this would need to be implemented)
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # For now, just test that we can get the user profile
        response = await client.get("/v1/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_superuser"] is True
    
    async def test_token_expiration_handling(self, client: AsyncClient, test_user: User):
        """Test handling of expired tokens."""
        # This test would require manipulating token expiration
        # For now, we'll test with an obviously invalid token
        
        headers = {"Authorization": "Bearer expired_token"}
        response = await client.get("/v1/auth/me", headers=headers)
        
        assert response.status_code == 401
        data = response.json()
        
        assert data["success"] is False
        assert data["error"] in ["TOKEN_INVALID", "UNAUTHORIZED"]


class TestHealthChecks:
    """Test health check endpoints."""
    
    async def test_health_check(self, client: AsyncClient):
        """Test comprehensive health check."""
        response = await client.get("/v1/health/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "status" in data
        assert "services" in data
        assert isinstance(data["services"], list)
    
    async def test_readiness_check(self, client: AsyncClient):
        """Test readiness check."""
        response = await client.get("/v1/health/ready")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "ready"
        assert "timestamp" in data
        assert "checks" in data
    
    async def test_liveness_check(self, client: AsyncClient):
        """Test liveness check."""
        response = await client.get("/v1/health/live")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "alive"
        assert "uptime_seconds" in data
        assert "timestamp" in data
    
    async def test_ping(self, client: AsyncClient):
        """Test simple ping."""
        response = await client.get("/v1/health/ping")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["message"] == "pong"


class TestErrorHandling:
    """Test error handling and responses."""
    
    async def test_validation_error(self, client: AsyncClient):
        """Test validation error handling."""
        # Invalid email format
        login_data = {
            "email": "invalid-email",
            "password": "password"
        }
        
        response = await client.post("/v1/auth/login", json=login_data)
        
        assert response.status_code == 422
        data = response.json()
        
        assert data["success"] is False
        assert data["error"] == "VALIDATION_ERROR"
        assert "details" in data
    
    async def test_not_found_error(self, client: AsyncClient):
        """Test not found error handling."""
        # Try to access non-existent endpoint
        response = await client.get("/v1/non-existent")
        
        assert response.status_code == 404
        data = response.json()
        
        assert data["success"] is False
        assert data["error"] == "NOT_FOUND"
    
    async def test_method_not_allowed(self, client: AsyncClient):
        """Test method not allowed error."""
        # Use wrong HTTP method
        response = await client.put("/v1/auth/login")
        
        assert response.status_code == 405
