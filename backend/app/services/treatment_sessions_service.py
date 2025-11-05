"""Service layer for treatment sessions domain."""

from app.db.models.treatment_session import TreatmentSession
from app.db.repositories.treatment_sessions_repo import TreatmentSessionsRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any, Dict

class TreatmentSessionsService:
    """Service for treatment sessions domain operations."""
    
    def __init__(self):
        self.repository = TreatmentSessionsRepository()

    async def create_treatment_session(self, db: AsyncSession, request_data: Dict[str, Any]) -> TreatmentSession:
        """Create new treatment session."""
        return await self.repository.create(db, request_data)
    
    async def list_treatment_sessions(self, db: AsyncSession, treatment_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[TreatmentSession]:
        """List all treatment sessions."""
        return await self.repository.get_all(db, treatment_id=treatment_id, skip=skip, limit=limit)
    
    async def get_treatment_session_by_id(self, db: AsyncSession, session_id: int) -> Optional[TreatmentSession]:
        """Get treatment session by ID."""
        return await self.repository.get_by_id(db, session_id)
    
    async def update_treatment_session(self, db: AsyncSession, session_id: int, request_data: Dict[str, Any]) -> Optional[TreatmentSession]:
        """Update treatment session by ID."""
        return await self.repository.update(db, session_id, request_data)
    
    async def delete_treatment_session(self, db: AsyncSession, session_id: int) -> bool:
        """Delete treatment session by ID."""
        return await self.repository.delete(db, session_id)

