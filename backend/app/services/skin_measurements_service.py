"""Service layer for skin measurements domain."""

from app.db.models.skin_color_measurement import SkinColorMeasurement
from app.db.repositories.skin_measurements_repo import SkinMeasurementsRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any, Dict

class SkinMeasurementsService:
    """Service for skin measurements domain operations."""
    
    def __init__(self):
        self.repository = SkinMeasurementsRepository()

    async def create_skin_measurement(self, db: AsyncSession, request_data: Dict[str, Any]) -> SkinColorMeasurement:
        """Create new skin measurement."""
        return await self.repository.create(db, request_data)
    
    async def list_skin_measurements(self, db: AsyncSession, session_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[SkinColorMeasurement]:
        """List all skin measurements."""
        return await self.repository.get_all(db, session_id=session_id, skip=skip, limit=limit)
    
    async def delete_skin_measurement(self, db: AsyncSession, measurement_id: int) -> bool:
        """Delete skin measurement by ID."""
        return await self.repository.delete(db, measurement_id)

