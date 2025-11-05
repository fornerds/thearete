"""FastAPI router for color recipes domain."""

from app.schemas.color_recipes_request import Request25 as color_recipes_request_25, Request26 as color_recipes_request_26
from app.schemas.color_recipes_response import Response25 as color_recipes_response_25, Response26 as color_recipes_response_26
from app.services.color_recipes_service import ColorRecipesService
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from typing import List, Optional

router = APIRouter(prefix="/api/v1", tags=["color-recipes"])

@router.post("/color-recipes", summary="컬러 레시피 등록")
async def create_api_v1_color_recipes(
    request: color_recipes_request_25,
    db: AsyncSession = Depends(get_db)
) -> color_recipes_response_25:
    """컬러 레시피 등록"""
    service = ColorRecipesService()
    request_dict = request.dict(exclude_unset=True)
    session_id = request_dict.pop("session_id")
    
    result = await service.create_color_recipe(db, session_id, request_dict)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treatment session not found"
        )
    return color_recipes_response_25(
        recipe_id=str(result.id),
        created_at=result.created_at.isoformat() if result.created_at else None
    )

@router.get("/color-recipes/{session_id}", summary="레시피 조회")
async def get_api_v1_color_recipes_by_session_id(
    session_id: int = Path(..., description="시술 회차 ID"),
    db: AsyncSession = Depends(get_db)
) -> color_recipes_response_26:
    """레시피 조회"""
    service = ColorRecipesService()
    result = await service.get_color_recipe_by_session_id(db, session_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treatment session not found"
        )
    return color_recipes_response_26(
        melanin=str(result.melanin) if result.melanin is not None else "0",
        white=str(result.white) if result.white is not None else "0",
        red=str(result.red) if result.red is not None else "0",
        yellow=str(result.yellow) if result.yellow is not None else "0"
    )
