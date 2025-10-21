"""Item service for business logic."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.db.models.item import Item
from app.db.repositories.item_repo import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    """Item service for business logic."""
    
    def __init__(self, db: Optional[Session] = None):
        self.db = db
    
    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        """Get item by ID."""
        if not self.db:
            return None
        repo = ItemRepository(self.db)
        return repo.get_item_by_id(item_id)
    
    def get_items(self, skip: int = 0, limit: int = 100, owner_id: Optional[int] = None) -> List[Item]:
        """Get items with pagination and optional owner filter."""
        if not self.db:
            return []
        repo = ItemRepository(self.db)
        return repo.get_items(skip=skip, limit=limit, owner_id=owner_id)
    
    def create_item(self, item_create: ItemCreate, owner_id: int) -> Item:
        """Create a new item."""
        if not self.db:
            raise ValueError("Database session required")
        
        repo = ItemRepository(self.db)
        return repo.create_item(item_create, owner_id)
    
    def update_item(self, item_id: int, item_update: ItemUpdate, owner_id: int) -> Item:
        """Update item (only by owner)."""
        if not self.db:
            raise ValueError("Database session required")
        
        repo = ItemRepository(self.db)
        
        # Check if item exists and belongs to owner
        existing_item = repo.get_item_by_id(item_id)
        if not existing_item:
            raise NotFoundException("Item not found")
        
        if existing_item.owner_id != owner_id:
            raise NotFoundException("Item not found")  # Don't reveal ownership
        
        return repo.update_item(item_id, item_update)
    
    def delete_item(self, item_id: int, owner_id: int) -> bool:
        """Delete item (only by owner)."""
        if not self.db:
            raise ValueError("Database session required")
        
        repo = ItemRepository(self.db)
        
        # Check if item exists and belongs to owner
        existing_item = repo.get_item_by_id(item_id)
        if not existing_item:
            return False
        
        if existing_item.owner_id != owner_id:
            return False  # Don't reveal ownership
        
        return repo.delete_item(item_id)
    
    def get_user_items(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
        """Get items owned by a specific user."""
        return self.get_items(skip=skip, limit=limit, owner_id=owner_id)
