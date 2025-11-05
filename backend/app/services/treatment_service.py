"""Service layer for treatment domain."""

from app.db.models.treatment import Treatment
from app.db.repositories.treatment_repo import TreatmentRepository
from app.schemas.treatment_request import Request11, Request12, Request14, Request15
from app.schemas.treatment_response import Response11, Response12, Response13, Response14, Response15
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any, Dict

class TreatmentService:
    """Service for treatment domain operations."""
    
    def __init__(self):
        self.repository = TreatmentRepository()

    async def create_treatment(self, db: AsyncSession, request_data: Dict[str, Any]) -> Treatment:
        """Create new treatment."""
        return await self.repository.create(db, request_data)
    
    async def list_treatments(self, db: AsyncSession, customer_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Treatment]:
        """List all treatments."""
        return await self.repository.get_all(db, skip=skip, limit=limit, customer_id=customer_id)
    
    async def get_treatment_by_id(self, db: AsyncSession, treatment_id: int) -> Optional[Treatment]:
        """Get treatment by ID."""
        return await self.repository.get_by_id(db, treatment_id)
    
    async def update_treatment(self, db: AsyncSession, treatment_id: int, request_data: Dict[str, Any]) -> Optional[Treatment]:
        """Update treatment by ID."""
        return await self.repository.update(db, treatment_id, request_data)
    
    async def complete_treatment(self, db: AsyncSession, treatment_id: int) -> bool:
        """Mark treatment as completed if all sessions are completed."""
        treatment = await self.repository.get_by_id(db, treatment_id)
        if not treatment:
            return False
        
        # Check if all treatment sessions are completed
        from app.db.models.treatment_session import TreatmentSession
        from sqlalchemy import select, func
        
        result = await db.execute(
            select(func.count(TreatmentSession.id))
            .where(TreatmentSession.treatment_id == treatment_id)
            .where(TreatmentSession.is_deleted == False)
        )
        total_sessions = result.scalar() or 0
        
        result = await db.execute(
            select(func.count(TreatmentSession.id))
            .where(TreatmentSession.treatment_id == treatment_id)
            .where(TreatmentSession.is_completed == True)
            .where(TreatmentSession.is_deleted == False)
        )
        completed_sessions = result.scalar() or 0
        
        if total_sessions > 0 and total_sessions == completed_sessions:
            await self.repository.update(db, treatment_id, {"is_completed": True})
            return True
        return False

