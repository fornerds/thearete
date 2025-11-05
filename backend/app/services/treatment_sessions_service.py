"""Service layer for treatment sessions domain."""

from app.db.models.treatment_session import TreatmentSession
from app.db.repositories.treatment_sessions_repo import TreatmentSessionsRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any, Dict

class TreatmentSessionsService:
    """Service for treatment sessions domain operations."""
    
    def __init__(self):
        self.repository = TreatmentSessionsRepository()

    async def create_treatment_session(self, db: AsyncSession, request_data: Dict[str, Any], shop_id: Optional[int] = None) -> TreatmentSession:
        """Create new treatment session."""
        # Verify that treatment belongs to the shop
        if shop_id:
            from app.db.models.treatment import Treatment
            from app.db.models.customer import Customer
            from sqlalchemy import select, or_
            from app.core.exceptions import ForbiddenException
            
            treatment_id = request_data.get("treatment_id")
            if treatment_id:
                result = await db.execute(
                    select(Treatment)
                    .join(Customer)
                    .where(Treatment.id == treatment_id)
                    .where(or_(Treatment.is_deleted == False, Treatment.is_deleted.is_(None)))
                    .where(Customer.shop_id == shop_id)
                )
                treatment = result.scalar_one_or_none()
                if not treatment:
                    raise ForbiddenException("Treatment not found or does not belong to your shop")
        
        return await self.repository.create(db, request_data)
    
    async def list_treatment_sessions(self, db: AsyncSession, treatment_id: Optional[int] = None, shop_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[TreatmentSession]:
        """List all treatment sessions."""
        return await self.repository.get_all(db, treatment_id=treatment_id, shop_id=shop_id, skip=skip, limit=limit)
    
    async def get_treatment_session_by_id(self, db: AsyncSession, session_id: int, shop_id: Optional[int] = None) -> Optional[TreatmentSession]:
        """Get treatment session by ID."""
        return await self.repository.get_by_id(db, session_id, shop_id=shop_id)
    
    async def update_treatment_session(self, db: AsyncSession, session_id: int, request_data: Dict[str, Any], shop_id: Optional[int] = None) -> Optional[TreatmentSession]:
        """Update treatment session by ID."""
        # Verify treatment session belongs to shop
        if shop_id:
            session = await self.get_treatment_session_by_id(db, session_id, shop_id=shop_id)
            if not session:
                return None
        return await self.repository.update(db, session_id, request_data)
    
    async def delete_treatment_session(self, db: AsyncSession, session_id: int, shop_id: Optional[int] = None) -> bool:
        """Delete treatment session by ID."""
        # Verify treatment session belongs to shop
        if shop_id:
            session = await self.get_treatment_session_by_id(db, session_id, shop_id=shop_id)
            if not session:
                return False
        return await self.repository.delete(db, session_id)

