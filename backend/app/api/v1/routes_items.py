"""Item routes with authentication."""

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.core.pagination import PaginationParams, PaginatedResponse
from app.deps import CurrentUserDep, DatabaseDep
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.services.item_service import ItemService

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[Item])
async def get_items(
    pagination: Annotated[PaginationParams, Depends()],
    db: DatabaseDep,
    current_user: CurrentUserDep,
) -> PaginatedResponse[Item]:
    """Get items with pagination."""
    item_service = ItemService(db)
    items = item_service.get_items(
        skip=pagination.offset,
        limit=pagination.size,
    )
    
    # In a real implementation, you would get the total count
    total = len(items)  # This is simplified
    
    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        size=pagination.size,
    )


@router.get("/my", response_model=PaginatedResponse[Item])
async def get_my_items(
    pagination: Annotated[PaginationParams, Depends()],
    db: DatabaseDep,
    current_user: CurrentUserDep,
) -> PaginatedResponse[Item]:
    """Get current user's items."""
    item_service = ItemService(db)
    items = item_service.get_user_items(
        owner_id=current_user.id,
        skip=pagination.offset,
        limit=pagination.size,
    )
    
    # In a real implementation, you would get the total count
    total = len(items)  # This is simplified
    
    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        size=pagination.size,
    )


@router.get("/{item_id}", response_model=Item)
async def get_item(
    item_id: int,
    db: DatabaseDep,
    current_user: CurrentUserDep,
) -> Item:
    """Get item by ID."""
    item_service = ItemService(db)
    item = item_service.get_item_by_id(item_id)
    
    if not item:
        raise NotFoundException("Item not found")
    
    return item


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_data: ItemCreate,
    db: DatabaseDep,
    current_user: CurrentUserDep,
) -> Item:
    """Create a new item."""
    item_service = ItemService(db)
    item = item_service.create_item(item_data, current_user.id)
    return item


@router.put("/{item_id}", response_model=Item)
async def update_item(
    item_id: int,
    item_data: ItemUpdate,
    db: DatabaseDep,
    current_user: CurrentUserDep,
) -> Item:
    """Update item (only by owner)."""
    item_service = ItemService(db)
    item = item_service.update_item(item_id, item_data, current_user.id)
    return item


@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    db: DatabaseDep,
    current_user: CurrentUserDep,
) -> JSONResponse:
    """Delete item (only by owner)."""
    item_service = ItemService(db)
    success = item_service.delete_item(item_id, current_user.id)
    
    if not success:
        raise NotFoundException("Item not found")
    
    return JSONResponse(
        content={"message": "Item deleted successfully"}
    )
