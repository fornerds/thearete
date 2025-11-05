"""Service layer for treatment photos domain."""

from app.db.models.photo import Photo
from app.db.repositories.treatment_photos_repo import TreatmentPhotosRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any, Dict

class TreatmentPhotosService:
    """Service for treatment photos domain operations."""
    
    def __init__(self):
        self.repository = TreatmentPhotosRepository()

    async def create_treatment_photo(self, db: AsyncSession, request_data: Dict[str, Any], shop_id: Optional[int] = None) -> Photo:
        """Create new treatment photo."""
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
            
            # If session_id is provided, verify it belongs to the shop
            session_id = request_data.get("session_id")
            if session_id:
                from app.db.models.treatment_session import TreatmentSession
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
    
    async def list_treatment_photos(self, db: AsyncSession, treatment_id: Optional[int] = None, session_id: Optional[int] = None, shop_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Photo]:
        """List all treatment photos."""
        return await self.repository.get_all(db, treatment_id=treatment_id, session_id=session_id, shop_id=shop_id, skip=skip, limit=limit)
    
    async def delete_treatment_photo(self, db: AsyncSession, photo_id: int, shop_id: Optional[int] = None) -> bool:
        """Delete treatment photo by ID."""
        # Verify photo belongs to shop
        if shop_id:
            photo = await self.repository.get_by_id(db, photo_id, shop_id=shop_id)
            if not photo:
                return False
        return await self.repository.delete(db, photo_id)

