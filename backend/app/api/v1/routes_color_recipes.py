"""FastAPI router for color recipes domain."""

from app.schemas.color_recipes_request import Request25 as color_recipes_request_25, Request26 as color_recipes_request_26
from app.schemas.color_recipes_response import Response25 as color_recipes_response_25, Response26 as color_recipes_response_26
from app.services.color_recipes_service import ColorRecipesService
from app.core.auth import get_current_shop
from app.db.models.shop import Shop
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from typing import List, Optional

router = APIRouter(prefix="/api/v1", tags=["color-recipes"])

@router.post("/color-recipes", summary="컬러 레시피 등록 (AI 추천)")
async def create_api_v1_color_recipes(
    request: color_recipes_request_25,
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> color_recipes_response_25:
    """
    컬러 레시피 등록 (AI 추천)
    
    피부색 측정 데이터를 기반으로 AI 모델이 color recipe를 추천합니다.
    - session_id로 해당 시술 회차의 피부색 측정 데이터를 조회
    - AI 모델 인터페이스를 통해 color recipe 추천 받기
    - 추천된 레시피를 TreatmentSession에 저장
    """
    service = ColorRecipesService()
    session_id = request.session_id
    
    result = await service.create_color_recipe(db, session_id, shop_id=current_shop.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treatment session not found or does not belong to your shop"
        )
    return color_recipes_response_25(
        recipe_id=str(result.id),
        created_at=result.created_at.isoformat() if result.created_at else None
    )

@router.get("/color-recipes/{session_id}", summary="레시피 조회")
async def get_api_v1_color_recipes_by_session_id(
    session_id: int = Path(..., description="시술 회차 ID"),
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> color_recipes_response_26:
    """레시피 조회 (로그인한 Shop의 레시피만 조회 가능)"""
    service = ColorRecipesService()
    result = await service.get_color_recipe_by_session_id(db, session_id, shop_id=current_shop.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treatment session not found or does not belong to your shop"
        )
    return color_recipes_response_26(
        melanin=str(result.melanin) if result.melanin is not None else "0",
        white=str(result.white) if result.white is not None else "0",
        red=str(result.red) if result.red is not None else "0",
        yellow=str(result.yellow) if result.yellow is not None else "0"
    )
