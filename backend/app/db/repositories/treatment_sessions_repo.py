"""Repository layer for treatment sessions domain."""

from app.db.models.treatment_session import TreatmentSession
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional, Any

class TreatmentSessionsRepository:
    """Repository for treatment sessions domain database operations."""
    
    async def get_by_id(self, db: AsyncSession, session_id: int) -> Optional[TreatmentSession]:
        """Get treatment session by ID."""
        result = await db.execute(
            select(TreatmentSession).where(TreatmentSession.id == session_id).where(TreatmentSession.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, db: AsyncSession, treatment_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[TreatmentSession]:
        """Get all treatment sessions with pagination."""
        query = select(TreatmentSession).where(TreatmentSession.is_deleted == False)
        if treatment_id:
            query = query.where(TreatmentSession.treatment_id == treatment_id)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, session_data: dict) -> TreatmentSession:
        """Create new treatment session."""
        session = TreatmentSession(**session_data)
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session
    
    async def update(self, db: AsyncSession, session_id: int, session_data: dict) -> Optional[TreatmentSession]:
        """Update treatment session by ID."""
        result = await db.execute(
            update(TreatmentSession)
            .where(TreatmentSession.id == session_id)
            .values(**session_data)
        )
        await db.commit()
        
        if result.rowcount > 0:
            return await self.get_by_id(db, session_id)
        return None
    
    async def delete(self, db: AsyncSession, session_id: int) -> bool:
        """Delete treatment session by ID (soft delete)."""
        result = await db.execute(
            update(TreatmentSession)
            .where(TreatmentSession.id == session_id)
            .values(is_deleted=True)
        )
        await db.commit()
        return result.rowcount > 0



