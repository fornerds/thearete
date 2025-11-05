"""Repository layer for shop domain."""

from app.db.models.shop import Shop
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional, Any

class ShopRepository:
    """Repository for shop domain database operations."""
    
    async def get_by_id(self, db: AsyncSession, shop_id: int) -> Optional[Shop]:
        """Get shop by ID."""
        result = await db.execute(
            select(Shop).where(Shop.id == shop_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[Shop]:
        """Get shop by email."""
        from sqlalchemy import or_
        result = await db.execute(
            select(Shop).where(
                Shop.email == email
            ).where(
                or_(Shop.is_deleted == False, Shop.is_deleted.is_(None))
            )
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Shop]:
        """Get all shops with pagination."""
        result = await db.execute(
            select(Shop).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, shop_data: dict) -> Shop:
        """Create new shop."""
        shop = Shop(**shop_data)
        db.add(shop)
        await db.commit()
        await db.refresh(shop)
        return shop
    
    async def update(self, db: AsyncSession, shop_id: int, shop_data: dict) -> Optional[Shop]:
        """Update shop by ID."""
        result = await db.execute(
            update(Shop)
            .where(Shop.id == shop_id)
            .values(**shop_data)
        )
        await db.commit()
        
        if result.rowcount > 0:
            return await self.get_by_id(db, shop_id)
        return None
    
    async def delete(self, db: AsyncSession, shop_id: int) -> bool:
        """Delete shop by ID."""
        result = await db.execute(
            delete(Shop).where(Shop.id == shop_id)
        )
        await db.commit()
        return result.rowcount > 0



