"""FastAPI router for skin measurements domain."""

from app.schemas.skin_measurements_request import Request22 as skin_measurements_request_22, Request23 as skin_measurements_request_23, Request24 as skin_measurements_request_24
from app.schemas.skin_measurements_response import Response22 as skin_measurements_response_22, Response23 as skin_measurements_response_23, Response24 as skin_measurements_response_24
from app.services.skin_measurements_service import SkinMeasurementsService
from app.core.auth import get_current_shop
from app.db.models.shop import Shop
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["skin-measurements"])

@router.post("/skin-measurements", summary="시술 회차별 피부색 데이터 등록")
async def create_api_v1_skin_measurements(
    request: skin_measurements_request_22,
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> skin_measurements_response_22:
    """시술 회차별 피부색 데이터 등록 (로그인한 Shop의 TreatmentSession에만 등록 가능)"""
    service = SkinMeasurementsService()
    request_dict = request.dict(exclude_unset=True)
    # Map type to region_type
    if "type" in request_dict:
        request_dict["region_type"] = request_dict.pop("type")
    # Map L, a, b to l_value, a_value, b_value
    if "L" in request_dict:
        request_dict["l_value"] = request_dict.pop("L")
    if "a" in request_dict:
        request_dict["a_value"] = request_dict.pop("a")
    if "b" in request_dict:
        request_dict["b_value"] = request_dict.pop("b")
    # Parse measured_at if provided
    if "measured_at" in request_dict and request_dict.get("measured_at"):
        request_dict["measured_at"] = datetime.fromisoformat(request_dict["measured_at"].replace("Z", "+00:00"))
    
    result = await service.create_skin_measurement(db, request_dict, shop_id=current_shop.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Skin measurement creation failed"
        )
    return skin_measurements_response_22(
        measurement_id=str(result.id),
        created_at=result.created_at.isoformat() if result.created_at else None
    )

@router.get("/skin-measurements", summary="회차별 측정 데이터 목록")
async def list_api_v1_skin_measurements(
    session_id: Optional[int] = None,
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
):
    """회차별 측정 데이터 목록 (로그인한 Shop의 측정 데이터만 조회)"""
    service = SkinMeasurementsService()
    measurements = await service.list_skin_measurements(db, session_id=session_id, shop_id=current_shop.id)
    
    measurements_list = [
        {
            "L": str(m.l_value) if m.l_value is not None else None,
            "a": str(m.a_value) if m.a_value is not None else None,
            "b": str(m.b_value) if m.b_value is not None else None,
            "type": m.region_type,
            "measurement_id": str(m.id),
            "session_id": m.session_id,
            "created_at": m.created_at.isoformat() if m.created_at else None
        }
        for m in measurements
    ]
    
    return {"measurements": measurements_list}

@router.delete("/skin-measurements/{id}", summary="측정 데이터 삭제")
async def delete_api_v1_skin_measurements_by_id(
    id: int = Path(..., description="측정 데이터 ID"),
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> skin_measurements_response_24:
    """측정 데이터 삭제 (로그인한 Shop의 측정 데이터만 삭제 가능)"""
    service = SkinMeasurementsService()
    success = await service.delete_skin_measurement(db, id, shop_id=current_shop.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skin measurement not found"
        )
    return skin_measurements_response_24(
        deleted_at=datetime.utcnow().isoformat()
    )
