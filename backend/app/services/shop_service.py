"""Service layer for shop domain."""

from app.db.models.shop import Shop
from app.db.repositories.shop_repo import ShopRepository
from app.core.security import get_password_hash
from app.schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any

class ShopService:
    """Service for shop domain operations."""
    
    def __init__(self):
        self.repository = ShopRepository()

    async def create_shop(self, db: AsyncSession, request_data: dict) -> Shop:
        """Create new shop."""
        # Hash password if provided
        if "password" in request_data and request_data["password"]:
            # 추가 안전장치: 비밀번호 길이 검증
            password_bytes = request_data["password"].encode('utf-8')
            if len(password_bytes) > 72:
                raise ValueError(
                    f"비밀번호는 최대 72바이트까지 허용됩니다. 현재 비밀번호는 {len(password_bytes)}바이트입니다."
                )
            request_data["password"] = get_password_hash(request_data["password"])
        return await self.repository.create(db, request_data)
    async def list_shops(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Shop]:
        """List all shops."""
        return await self.repository.get_all(db, skip=skip, limit=limit)
    async def get_shop_by_id(self, db: AsyncSession, shop_id: int) -> Optional[Shop]:
        """Get shop by ID."""
        return await self.repository.get_by_id(db, shop_id)
    
    async def get_shop_by_email(self, db: AsyncSession, email: str) -> Optional[Shop]:
        """Get shop by email."""
        return await self.repository.get_by_email(db, email)
    async def update_shop(self, db: AsyncSession, shop_id: int, request_data: dict) -> Optional[Shop]:
        """Update shop by ID."""
        return await self.repository.update(db, shop_id, request_data)
    async def delete_shop(self, db: AsyncSession, shop_id: int) -> bool:
        """Delete shop by ID."""
        return await self.repository.delete(db, shop_id)

