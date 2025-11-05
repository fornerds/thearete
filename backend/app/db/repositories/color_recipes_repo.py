"""Repository layer for color recipes domain."""

from app.db.models.color_recipes import ColorRecipes
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional, Any

class ColorRecipesRepository:
    """Repository for color recipes domain database operations."""
    
    async def get_by_id(self, db: AsyncSession, color_recipes_id: int) -> Optional[ColorRecipes]:
        """Get color_recipes by ID."""
        result = await db.execute(
            select(ColorRecipes).where(ColorRecipes.id == color_recipes_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ColorRecipes]:
        """Get all color_recipess with pagination."""
        result = await db.execute(
            select(ColorRecipes).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, color_recipes_data: dict) -> ColorRecipes:
        """Create new color_recipes."""
        color_recipes = ColorRecipes(**color_recipes_data)
        db.add(color_recipes)
        await db.commit()
        await db.refresh(color_recipes)
        return color_recipes
    
    async def update(self, db: AsyncSession, color_recipes_id: int, color_recipes_data: dict) -> Optional[ColorRecipes]:
        """Update color_recipes by ID."""
        result = await db.execute(
            update(ColorRecipes)
            .where(ColorRecipes.id == color_recipes_id)
            .values(**color_recipes_data)
        )
        await db.commit()
        
        if result.rowcount > 0:
            return await self.get_by_id(db, color_recipes_id)
        return None
    
    async def delete(self, db: AsyncSession, color_recipes_id: int) -> bool:
        """Delete color_recipes by ID."""
        result = await db.execute(
            delete(ColorRecipes).where(ColorRecipes.id == color_recipes_id)
        )
        await db.commit()
        return result.rowcount > 0



