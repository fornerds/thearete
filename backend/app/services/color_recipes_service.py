"""Service layer for color recipes domain."""

from app.db.models.treatment_session import TreatmentSession
from app.db.repositories.treatment_sessions_repo import TreatmentSessionsRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any, Dict

class ColorRecipesService:
    """Service for color recipes domain operations."""
    
    def __init__(self):
        self.repository = TreatmentSessionsRepository()

    async def create_color_recipe(self, db: AsyncSession, session_id: int, request_data: Dict[str, Any]) -> TreatmentSession:
        """Create/update color recipe for a treatment session."""
        color_data = {
            "melanin": request_data.get("melanin"),
            "white": request_data.get("white"),
            "red": request_data.get("red"),
            "yellow": request_data.get("yellow")
        }
        return await self.repository.update(db, session_id, color_data)
    
    async def get_color_recipe_by_session_id(self, db: AsyncSession, session_id: int) -> Optional[TreatmentSession]:
        """Get color recipe by session ID."""
        return await self.repository.get_by_id(db, session_id)

