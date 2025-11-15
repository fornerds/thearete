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

    async def create_treatment(self, db: AsyncSession, request_data: Dict[str, Any], shop_id: Optional[int] = None) -> Treatment:
        """Create new treatment and first treatment session with images."""
        # Verify that customer belongs to the shop
        if shop_id:
            from app.db.models.customer import Customer
            from sqlalchemy import select
            from app.core.exceptions import ForbiddenException
            
            customer_id = request_data.get("customer_id")
            if customer_id:
                result = await db.execute(
                    select(Customer).where(Customer.id == customer_id)
                )
                customer = result.scalar_one_or_none()
                if not customer:
                    raise ForbiddenException("Customer not found")
                if customer.shop_id != shop_id:
                    raise ForbiddenException("Customer does not belong to your shop")
        
        # Extract images from request_data
        images_payload = request_data.pop("images", [])
        
        # Create treatment
        treatment = await self.repository.create(db, request_data)
        
        # Create first treatment session automatically
        from app.services.treatment_sessions_service import TreatmentSessionsService
        from datetime import datetime
        
        session_service = TreatmentSessionsService()
        # First session always has sequence = 1
        # Generate session_name: {type}({area})/{sequence}차
        treatment_type = treatment.type or ""
        treatment_area = treatment.area or ""
        session_name = f"{treatment_type}({treatment_area})/1차"
        
        session_data = {
            "treatment_id": treatment.id,
            "sequence": 1,
            "session_name": session_name,
            "treatment_date": datetime.utcnow().date(),
            "is_completed": False,
        }
        
        session = await session_service.repository.create(db, session_data)
        
        # Connect images to the first session if provided
        if images_payload:
            # Convert Pydantic models to dict if needed
            images_dict = []
            for img in images_payload:
                if isinstance(img, dict):
                    images_dict.append(img)
                else:
                    images_dict.append(img.dict() if hasattr(img, 'dict') else img)
            
            await session_service.set_session_images(
                db,
                treatment_id=treatment.id,
                session_id=session.id,
                images_payload=images_dict,
            )
        
        # Refresh treatment to get updated relationships
        await db.refresh(treatment)
        return treatment
    
    async def list_treatments(self, db: AsyncSession, customer_id: Optional[int] = None, shop_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Treatment]:
        """List all treatments."""
        return await self.repository.get_all(db, skip=skip, limit=limit, customer_id=customer_id, shop_id=shop_id)
    
    async def get_treatment_by_id(self, db: AsyncSession, treatment_id: int, shop_id: Optional[int] = None) -> Optional[Treatment]:
        """Get treatment by ID."""
        return await self.repository.get_by_id(db, treatment_id, shop_id=shop_id)
    
    async def update_treatment(self, db: AsyncSession, treatment_id: int, request_data: Dict[str, Any], shop_id: Optional[int] = None) -> Optional[Treatment]:
        """Update treatment by ID."""
        # Verify treatment belongs to shop
        if shop_id:
            treatment = await self.get_treatment_by_id(db, treatment_id, shop_id=shop_id)
            if not treatment:
                return None
        return await self.repository.update(db, treatment_id, request_data)
    
    async def complete_treatment(self, db: AsyncSession, treatment_id: int, shop_id: Optional[int] = None) -> bool:
        """Mark treatment as completed if all sessions are completed."""
        # Verify treatment belongs to shop
        if shop_id:
            treatment = await self.get_treatment_by_id(db, treatment_id, shop_id=shop_id)
        else:
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

