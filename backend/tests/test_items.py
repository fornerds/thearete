"""Item CRUD tests."""

import pytest
from fastapi import status


def test_create_item(client, auth_headers):
    """Test creating an item."""
    item_data = {
        "title": "Test Item",
        "description": "A test item",
        "price": 19.99
    }
    
    response = client.post(
        "/v1/items/",
        json=item_data,
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["description"] == item_data["description"]
    assert data["price"] == item_data["price"]
    assert "id" in data
    assert "owner_id" in data


def test_create_item_unauthorized(client):
    """Test creating an item without authentication."""
    item_data = {
        "title": "Test Item",
        "description": "A test item",
        "price": 19.99
    }
    
    response = client.post("/v1/items/", json=item_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_items(client, auth_headers):
    """Test getting items."""
    response = client.get("/v1/items/", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data


def test_get_my_items(client, auth_headers):
    """Test getting current user's items."""
    response = client.get("/v1/items/my", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data


def test_get_item_by_id(client, auth_headers):
    """Test getting an item by ID."""
    # First create an item
    item_data = {
        "title": "Test Item",
        "description": "A test item",
        "price": 19.99
    }
    
    create_response = client.post(
        "/v1/items/",
        json=item_data,
        headers=auth_headers
    )
    
    item_id = create_response.json()["id"]
    
    # Get the item
    response = client.get(f"/v1/items/{item_id}", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == item_id
    assert data["title"] == item_data["title"]


def test_get_nonexistent_item(client, auth_headers):
    """Test getting a non-existent item."""
    response = client.get("/v1/items/99999", headers=auth_headers)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_item(client, auth_headers):
    """Test updating an item."""
    # First create an item
    item_data = {
        "title": "Test Item",
        "description": "A test item",
        "price": 19.99
    }
    
    create_response = client.post(
        "/v1/items/",
        json=item_data,
        headers=auth_headers
    )
    
    item_id = create_response.json()["id"]
    
    # Update the item
    update_data = {
        "title": "Updated Item",
        "price": 29.99
    }
    
    response = client.put(
        f"/v1/items/{item_id}",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["price"] == update_data["price"]


def test_delete_item(client, auth_headers):
    """Test deleting an item."""
    # First create an item
    item_data = {
        "title": "Test Item",
        "description": "A test item",
        "price": 19.99
    }
    
    create_response = client.post(
        "/v1/items/",
        json=item_data,
        headers=auth_headers
    )
    
    item_id = create_response.json()["id"]
    
    # Delete the item
    response = client.delete(f"/v1/items/{item_id}", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Item deleted successfully"
    
    # Verify item is deleted
    get_response = client.get(f"/v1/items/{item_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
