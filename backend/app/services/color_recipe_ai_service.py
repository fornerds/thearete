"""AI service interface for color recipe recommendation."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class SkinMeasurementData:
    """Skin color measurement data structure."""
    l_value: Optional[float]
    a_value: Optional[float]
    b_value: Optional[float]
    region_type: Optional[str]  # "NORMAL" or "LESION"
    measurement_point: Optional[str] = None


@dataclass
class ColorRecipeRecommendation:
    """Color recipe recommendation result."""
    melanin: int  # 0~9
    white: int    # 0~9
    red: int      # 0~9
    yellow: int   # 0~9


class ColorRecipeAIService(ABC):
    """Abstract interface for color recipe AI recommendation service."""
    
    @abstractmethod
    async def recommend_color_recipe(
        self,
        measurements: List[SkinMeasurementData]
    ) -> ColorRecipeRecommendation:
        """
        Recommend color recipe based on skin color measurements.
        
        Args:
            measurements: List of skin color measurement data
            
        Returns:
            ColorRecipeRecommendation: Recommended color recipe (melanin, white, red, yellow)
            
        Raises:
            AIError: If the recommendation request fails
        """
        pass


class MockColorRecipeAIService(ColorRecipeAIService):
    """Mock implementation of ColorRecipeAIService for development/testing."""
    
    async def recommend_color_recipe(
        self,
        measurements: List[SkinMeasurementData]
    ) -> ColorRecipeRecommendation:
        """
        Mock implementation that returns default values.
        In production, this would call the actual AI model.
        """
        # Default values - 실제 구현 시 AI 모델 호출로 대체
        if not measurements:
            return ColorRecipeRecommendation(
                melanin=5,
                white=5,
                red=5,
                yellow=5
            )
        
        # 간단한 로직: L 값이 낮으면 (어두우면) melanin 증가, 높으면 white 증가
        avg_l = sum(m.l_value or 0 for m in measurements) / len(measurements) if measurements else 0
        avg_a = sum(m.a_value or 0 for m in measurements) / len(measurements) if measurements else 0
        avg_b = sum(m.b_value or 0 for m in measurements) / len(measurements) if measurements else 0
        
        # Mock calculation (실제 AI 모델 로직으로 대체 필요)
        melanin = max(0, min(9, int(5 + (50 - avg_l) / 10)))
        white = max(0, min(9, int(5 + (avg_l - 50) / 10)))
        red = max(0, min(9, int(5 + avg_a / 5)))
        yellow = max(0, min(9, int(5 + avg_b / 5)))
        
        return ColorRecipeRecommendation(
            melanin=melanin,
            white=white,
            red=red,
            yellow=yellow
        )


def get_color_recipe_ai_service() -> ColorRecipeAIService:
    """
    Factory function to get ColorRecipeAIService instance.
    In production, this would return the actual AI service implementation.
    """
    # TODO: 실제 AI 모델 서비스 구현 시 여기서 반환
    # 예: return OpenAIColorRecipeService() 또는 CustomAIColorRecipeService()
    return MockColorRecipeAIService()

