"""Service layer for shop domain."""

from app.db.models.shop import Shop
from app.db.repositories.shop_repo import ShopRepository
from app.schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any

class ShopService:
    """Service for shop domain operations."""
    
    def __init__(self):
        self.repository = ShopRepository()

    async def create_shop(self, request_data: dict) -> Shop:
        """Create new shop."""
        return await self.repository.create(request_data)
    async def list_shops(self, skip: int = 0, limit: int = 100) -> List[Shop]:
        """List all shops."""
        return await self.repository.get_all(skip=skip, limit=limit)
    async def get_shop_by_id(self, shop_id: int) -> Optional[Shop]:
        """Get shop by ID."""
        return await self.repository.get_by_id(shop_id)
    async def update_shop(self, shop_id: int, request_data: dict) -> Optional[Shop]:
        """Update shop by ID."""
        return await self.repository.update(shop_id, request_data)
    async def delete_shop(self, shop_id: int) -> bool:
        """Delete shop by ID."""
        return await self.repository.delete(shop_id)

