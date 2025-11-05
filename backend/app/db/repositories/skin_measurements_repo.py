"""Repository layer for skin measurements domain."""

from app.db.models.skin_color_measurement import SkinColorMeasurement
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any

class SkinMeasurementsRepository:
    """Repository for skin measurements domain database operations."""
    
    async def get_by_id(self, db: AsyncSession, measurement_id: int) -> Optional[SkinColorMeasurement]:
        """Get skin measurement by ID."""
        result = await db.execute(
            select(SkinColorMeasurement).where(SkinColorMeasurement.id == measurement_id).where(SkinColorMeasurement.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, db: AsyncSession, session_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[SkinColorMeasurement]:
        """Get all skin measurements with pagination."""
        query = select(SkinColorMeasurement).where(SkinColorMeasurement.is_deleted == False)
        if session_id:
            query = query.where(SkinColorMeasurement.session_id == session_id)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, measurement_data: dict) -> SkinColorMeasurement:
        """Create new skin measurement."""
        measurement = SkinColorMeasurement(**measurement_data)
        db.add(measurement)
        await db.commit()
        await db.refresh(measurement)
        return measurement
    
    async def delete(self, db: AsyncSession, measurement_id: int) -> bool:
        """Delete skin measurement by ID (soft delete)."""
        result = await db.execute(
            update(SkinColorMeasurement)
            .where(SkinColorMeasurement.id == measurement_id)
            .values(is_deleted=True)
        )
        await db.commit()
        return result.rowcount > 0



