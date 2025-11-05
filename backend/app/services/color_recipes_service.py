"""Service layer for color recipes domain."""

from app.db.models.treatment_session import TreatmentSession
from app.db.repositories.treatment_sessions_repo import TreatmentSessionsRepository
from app.db.repositories.skin_measurements_repo import SkinMeasurementsRepository
from app.services.color_recipe_ai_service import (
    ColorRecipeAIService,
    SkinMeasurementData,
    get_color_recipe_ai_service
)
from app.core.exceptions import ForbiddenException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any, Dict

class ColorRecipesService:
    """Service for color recipes domain operations."""
    
    def __init__(self):
        self.session_repository = TreatmentSessionsRepository()
        self.measurement_repository = SkinMeasurementsRepository()
        self.ai_service: ColorRecipeAIService = get_color_recipe_ai_service()

    async def create_color_recipe(
        self, 
        db: AsyncSession, 
        session_id: int, 
        shop_id: Optional[int] = None
    ) -> TreatmentSession:
        """
        Create/update color recipe for a treatment session using AI recommendation.
        
        Args:
            db: Database session
            session_id: Treatment session ID
            shop_id: Shop ID for authentication
            
        Returns:
            TreatmentSession: Updated treatment session with color recipe
            
        Raises:
            ForbiddenException: If session does not belong to the shop
        """
        # Verify session belongs to shop
        session = await self.session_repository.get_by_id(db, session_id, shop_id=shop_id)
        if not session:
            raise ForbiddenException("Treatment session not found or does not belong to your shop")
        
        # Get skin color measurements for this session
        measurements = await self.measurement_repository.get_all(
            db, 
            session_id=session_id, 
            shop_id=shop_id
        )
        
        if not measurements:
            raise ForbiddenException("No skin color measurements found for this session")
        
        # Convert measurements to SkinMeasurementData format
        measurement_data_list = [
            SkinMeasurementData(
                l_value=m.l_value,
                a_value=m.a_value,
                b_value=m.b_value,
                region_type=m.region_type,
                measurement_point=m.measurement_point
            )
            for m in measurements
        ]
        
        # Call AI service to get color recipe recommendation
        recommendation = await self.ai_service.recommend_color_recipe(measurement_data_list)
        
        # Update treatment session with recommended color recipe
        color_data = {
            "melanin": recommendation.melanin,
            "white": recommendation.white,
            "red": recommendation.red,
            "yellow": recommendation.yellow
        }
        
        updated_session = await self.session_repository.update(db, session_id, color_data)
        if not updated_session:
            raise ForbiddenException("Failed to update color recipe")
        
        return updated_session
    
    async def get_color_recipe_by_session_id(
        self, 
        db: AsyncSession, 
        session_id: int,
        shop_id: Optional[int] = None
    ) -> Optional[TreatmentSession]:
        """
        Get color recipe by session ID.
        
        Args:
            db: Database session
            session_id: Treatment session ID
            shop_id: Shop ID for authentication
            
        Returns:
            TreatmentSession: Treatment session with color recipe, or None if not found
        """
        return await self.session_repository.get_by_id(db, session_id, shop_id=shop_id)

