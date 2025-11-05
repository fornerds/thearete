"""Repository layer for treatment domain."""

from app.db.models.treatment import Treatment
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional, Any

class TreatmentRepository:
    """Repository for treatment domain database operations."""
    
    async def get_by_id(self, db: AsyncSession, treatment_id: int) -> Optional[Treatment]:
        """Get treatment by ID."""
        result = await db.execute(
            select(Treatment).where(Treatment.id == treatment_id).where(Treatment.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100, customer_id: Optional[int] = None) -> List[Treatment]:
        """Get all treatments with pagination."""
        query = select(Treatment).where(Treatment.is_deleted == False)
        if customer_id:
            query = query.where(Treatment.customer_id == customer_id)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_customer_id(self, db: AsyncSession, customer_id: int) -> List[Treatment]:
        """Get treatments by customer ID."""
        result = await db.execute(
            select(Treatment).where(Treatment.customer_id == customer_id).where(Treatment.is_deleted == False)
        )
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, treatment_data: dict) -> Treatment:
        """Create new treatment."""
        treatment = Treatment(**treatment_data)
        db.add(treatment)
        await db.commit()
        await db.refresh(treatment)
        return treatment
    
    async def update(self, db: AsyncSession, treatment_id: int, treatment_data: dict) -> Optional[Treatment]:
        """Update treatment by ID."""
        result = await db.execute(
            update(Treatment)
            .where(Treatment.id == treatment_id)
            .values(**treatment_data)
        )
        await db.commit()
        
        if result.rowcount > 0:
            return await self.get_by_id(db, treatment_id)
        return None
    
    async def delete(self, db: AsyncSession, treatment_id: int) -> bool:
        """Delete treatment by ID (soft delete)."""
        result = await db.execute(
            update(Treatment)
            .where(Treatment.id == treatment_id)
            .values(is_deleted=True)
        )
        await db.commit()
        return result.rowcount > 0



