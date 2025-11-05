"""Service layer for treatment photos domain."""

from app.db.models.photo import Photo
from app.db.repositories.treatment_photos_repo import TreatmentPhotosRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any, Dict

class TreatmentPhotosService:
    """Service for treatment photos domain operations."""
    
    def __init__(self):
        self.repository = TreatmentPhotosRepository()

    async def create_treatment_photo(self, db: AsyncSession, request_data: Dict[str, Any]) -> Photo:
        """Create new treatment photo."""
        return await self.repository.create(db, request_data)
    
    async def list_treatment_photos(self, db: AsyncSession, treatment_id: Optional[int] = None, session_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Photo]:
        """List all treatment photos."""
        return await self.repository.get_all(db, treatment_id=treatment_id, session_id=session_id, skip=skip, limit=limit)
    
    async def delete_treatment_photo(self, db: AsyncSession, photo_id: int) -> bool:
        """Delete treatment photo by ID."""
        return await self.repository.delete(db, photo_id)

