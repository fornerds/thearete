"""Authentication tests."""

import pytest
from fastapi import status


def test_login_success(client, test_user):
    """Test successful login."""
    response = client.post(
        "/v1/auth/login",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post(
        "/v1/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert "error" in data


def test_login_nonexistent_user(client):
    """Test login with non-existent user."""
    response = client.post(
        "/v1/auth/login",
        json={"email": "nonexistent@example.com", "password": "password"}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_token_success(client, test_user):
    """Test successful token refresh."""
    # First login
    login_response = client.post(
        "/v1/auth/login",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    
    refresh_token = login_response.json()["refresh_token"]
    
    # Refresh token
    response = client.post(
        "/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_refresh_token_invalid(client):
    """Test refresh with invalid token."""
    response = client.post(
        "/v1/auth/refresh",
        json={"refresh_token": "invalid_token"}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout(client, auth_headers):
    """Test logout endpoint."""
    response = client.post("/v1/auth/logout", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Successfully logged out"
