"""FastAPI router for treatment sessions domain."""

from app.schemas.treatment_sessions_request import Request16 as treatment_sessions_request_16, Request17 as treatment_sessions_request_17, Request18 as treatment_sessions_request_18, Request19 as treatment_sessions_request_19, Request20 as treatment_sessions_request_20, Request21 as treatment_sessions_request_21
from app.schemas.treatment_sessions_response import Response16 as treatment_sessions_response_16, Response17 as treatment_sessions_response_17, Response18 as treatment_sessions_response_18, Response19 as treatment_sessions_response_19, Response20 as treatment_sessions_response_20, Response21 as treatment_sessions_response_21
from app.services.treatment_sessions_service import TreatmentSessionsService
from app.core.auth import get_current_shop
from app.db.models.shop import Shop
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["treatment-sessions"])

@router.post("/treatment-sessions", summary="회차별 시술 기록")
async def create_api_v1_treatment_sessions(
    request: treatment_sessions_request_16,
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> treatment_sessions_response_16:
    """회차별 시술 기록 (로그인한 Shop의 Treatment에만 세션 등록 가능)"""
    service = TreatmentSessionsService()
    request_dict = request.dict(exclude_unset=True)
    # Map date to treatment_date
    if "date" in request_dict:
        date_str = request_dict.pop("date")
        if date_str:
            try:
                # Try parsing as ISO format first
                if "T" in date_str or "Z" in date_str:
                    request_dict["treatment_date"] = datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
                else:
                    # Parse as YYYY-MM-DD
                    request_dict["treatment_date"] = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format. Use YYYY-MM-DD")
        else:
            request_dict["treatment_date"] = None
    # Map duration to duration_minutes
    if "duration" in request_dict:
        request_dict["duration_minutes"] = int(request_dict.pop("duration")) if request_dict.get("duration") else None
    
    result = await service.create_treatment_session(db, request_dict, shop_id=current_shop.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Treatment session creation failed"
        )
    return treatment_sessions_response_16(
        session_id=str(result.id),
        created_at=result.created_at.isoformat() if result.created_at else None
    )

@router.get("/treatment-sessions", summary="회차 리스트")
async def list_api_v1_treatment_sessions(
    treatment_id: Optional[int] = None,
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
):
    """회차 리스트 (로그인한 Shop의 Treatment 세션만 조회)"""
    service = TreatmentSessionsService()
    sessions = await service.list_treatment_sessions(db, treatment_id=treatment_id, shop_id=current_shop.id)
    
    sessions_list = [
        {
            "session_id": str(s.id),
            "treatment_id": s.treatment_id,
            "date": s.treatment_date.isoformat() if s.treatment_date else None,
            "duration": s.duration_minutes,
            "is_completed": s.is_completed,
            "created_at": s.created_at.isoformat() if s.created_at else None
        }
        for s in sessions
    ]
    
    return {"sessions": sessions_list}

@router.get("/treatment-sessions/{id}", summary="회차 상세")
async def get_api_v1_treatment_sessions_by_id(
    id: int = Path(..., description="회차 ID"),
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> treatment_sessions_response_18:
    """회차 상세 (로그인한 Shop의 세션만 조회 가능)"""
    service = TreatmentSessionsService()
    result = await service.get_treatment_session_by_id(db, id, shop_id=current_shop.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treatment session not found"
        )
    return treatment_sessions_response_18(
        session_id=str(result.id),
        duration=str(result.duration_minutes) if result.duration_minutes else None,
        note=result.note
    )

@router.put("/treatment-sessions/{id}", summary="회차 정보 수정")
async def update_api_v1_treatment_sessions_by_id(
    id: int = Path(..., description="회차 ID"),
    request: treatment_sessions_request_19 = ...,
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> treatment_sessions_response_19:
    """회차 정보 수정 (로그인한 Shop의 세션만 수정 가능)"""
    service = TreatmentSessionsService()
    request_dict = request.dict(exclude_unset=True)
    # Map duration to duration_minutes
    if "duration" in request_dict:
        request_dict["duration_minutes"] = int(request_dict.pop("duration")) if request_dict.get("duration") else None
    # Map date to treatment_date if provided
    if "date" in request_dict and request_dict["date"]:
        try:
            date_str = request_dict.pop("date")
            if "T" in date_str or "Z" in date_str:
                request_dict["treatment_date"] = datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
            else:
                request_dict["treatment_date"] = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format. Use YYYY-MM-DD")
    
    result = await service.update_treatment_session(db, id, request_dict, shop_id=current_shop.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treatment session not found"
        )
    return treatment_sessions_response_19(
        updated_at=result.updated_at.isoformat() if result.updated_at else None
    )

@router.delete("/treatment-sessions/{id}", summary="회차 삭제")
async def delete_api_v1_treatment_sessions_by_id(
    id: int = Path(..., description="회차 ID"),
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> treatment_sessions_response_20:
    """회차 삭제 (로그인한 Shop의 세션만 삭제 가능)"""
    service = TreatmentSessionsService()
    success = await service.delete_treatment_session(db, id, shop_id=current_shop.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treatment session not found"
        )
    return treatment_sessions_response_20(
        deleted_at=datetime.utcnow().isoformat()
    )

@router.patch("/treatment-sessions/{id}/complete", summary="결과 입력 완료 표시")
async def patch_api_v1_treatment_sessions_by_id_complete(
    id: int = Path(..., description="회차 ID"),
    request: treatment_sessions_request_21 = ...,
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> treatment_sessions_response_21:
    """결과 입력 완료 표시 (로그인한 Shop의 세션만 완료 처리 가능)"""
    service = TreatmentSessionsService()
    is_result_entered = int(request.is_result_entered) if request.is_result_entered else 0
    request_dict = {"is_result_entered": is_result_entered}
    result = await service.update_treatment_session(db, id, request_dict, shop_id=current_shop.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treatment session not found"
        )
    return treatment_sessions_response_21(
        session_id=str(result.id),
        is_result_entered=str(result.is_result_entered) if result.is_result_entered else "0",
        message="Result entry status updated successfully"
    )
