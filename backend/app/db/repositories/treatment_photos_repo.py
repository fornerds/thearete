"""Repository layer for treatment photos domain."""

from app.db.models.photo import Photo
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any

class TreatmentPhotosRepository:
    """Repository for treatment photos domain database operations."""
    
    async def get_by_id(self, db: AsyncSession, photo_id: int, shop_id: Optional[int] = None) -> Optional[Photo]:
        """Get photo by ID."""
        from app.db.models.treatment import Treatment
        from app.db.models.customer import Customer
        from sqlalchemy import or_
        
        query = select(Photo).join(Treatment).join(Customer).where(
            Photo.id == photo_id
        ).where(or_(Photo.is_deleted == False, Photo.is_deleted.is_(None)))
        query = query.where(or_(Treatment.is_deleted == False, Treatment.is_deleted.is_(None)))
        
        if shop_id:
            query = query.where(Customer.shop_id == shop_id)
        
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all(self, db: AsyncSession, treatment_id: Optional[int] = None, session_id: Optional[int] = None, shop_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Photo]:
        """Get all photos with pagination."""
        from app.db.models.treatment import Treatment
        from app.db.models.customer import Customer
        from sqlalchemy import or_
        
        query = select(Photo).join(Treatment).join(Customer).where(
            or_(Photo.is_deleted == False, Photo.is_deleted.is_(None))
        )
        query = query.where(or_(Treatment.is_deleted == False, Treatment.is_deleted.is_(None)))
        
        if treatment_id:
            query = query.where(Photo.treatment_id == treatment_id)
        if session_id:
            query = query.where(Photo.session_id == session_id)
        
        if shop_id:
            query = query.where(Customer.shop_id == shop_id)
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, photo_data: dict) -> Photo:
        """Create new photo."""
        photo = Photo(**photo_data)
        db.add(photo)
        await db.commit()
        await db.refresh(photo)
        return photo
    
    async def delete(self, db: AsyncSession, photo_id: int) -> bool:
        """Delete photo by ID (soft delete)."""
        result = await db.execute(
            update(Photo)
            .where(Photo.id == photo_id)
            .values(is_deleted=True)
        )
        await db.commit()
        return result.rowcount > 0



