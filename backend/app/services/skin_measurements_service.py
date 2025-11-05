"""Service layer for skin measurements domain."""

from app.db.models.skin_color_measurement import SkinColorMeasurement
from app.db.repositories.skin_measurements_repo import SkinMeasurementsRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any, Dict

class SkinMeasurementsService:
    """Service for skin measurements domain operations."""
    
    def __init__(self):
        self.repository = SkinMeasurementsRepository()

    async def create_skin_measurement(self, db: AsyncSession, request_data: Dict[str, Any], shop_id: Optional[int] = None) -> SkinColorMeasurement:
        """Create new skin measurement."""
        # Verify that treatment session belongs to the shop
        if shop_id:
            from app.db.models.treatment_session import TreatmentSession
            from app.db.models.treatment import Treatment
            from app.db.models.customer import Customer
            from sqlalchemy import select, or_
            from app.core.exceptions import ForbiddenException
            
            session_id = request_data.get("session_id")
            if session_id:
                result = await db.execute(
                    select(TreatmentSession)
                    .join(Treatment)
                    .join(Customer)
                    .where(TreatmentSession.id == session_id)
                    .where(or_(TreatmentSession.is_deleted == False, TreatmentSession.is_deleted.is_(None)))
                    .where(or_(Treatment.is_deleted == False, Treatment.is_deleted.is_(None)))
                    .where(Customer.shop_id == shop_id)
                )
                session = result.scalar_one_or_none()
                if not session:
                    raise ForbiddenException("Treatment session not found or does not belong to your shop")
        
        return await self.repository.create(db, request_data)
    
    async def list_skin_measurements(self, db: AsyncSession, session_id: Optional[int] = None, shop_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[SkinColorMeasurement]:
        """List all skin measurements."""
        return await self.repository.get_all(db, session_id=session_id, shop_id=shop_id, skip=skip, limit=limit)
    
    async def delete_skin_measurement(self, db: AsyncSession, measurement_id: int, shop_id: Optional[int] = None) -> bool:
        """Delete skin measurement by ID."""
        # Verify skin measurement belongs to shop
        if shop_id:
            measurement = await self.repository.get_by_id(db, measurement_id, shop_id=shop_id)
            if not measurement:
                return False
        return await self.repository.delete(db, measurement_id)

