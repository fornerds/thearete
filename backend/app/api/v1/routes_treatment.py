"""FastAPI router for treatment domain."""

from app.schemas.treatment_request import Request11 as treatment_request_11, Request12 as treatment_request_12, Request13 as treatment_request_13, Request14 as treatment_request_14, Request15 as treatment_request_15
from app.schemas.treatment_response import Response11 as treatment_response_11, Response12 as treatment_response_12, Response13 as treatment_response_13, Response14 as treatment_response_14, Response15 as treatment_response_15
from app.services.treatment_service import TreatmentService
from app.core.auth import get_current_shop
from app.db.models.shop import Shop
from app.core.exceptions import ForbiddenException
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from typing import List, Optional

router = APIRouter(prefix="/v1", tags=["treatment"])


def _serialize_treatment_sessions(treatment) -> List[dict]:
    """Serialize treatment sessions with images."""
    sessions = getattr(treatment, "treatment_session", []) or []
    serialized = []
    for session in sessions:
        # Skip deleted sessions
        if getattr(session, "is_deleted", False) is True:
            continue
        
        images = getattr(session, "images", []) or []
        session_images = []
        for mapping in sorted(images, key=lambda item: item.sequence_no if item.sequence_no is not None else 0):
            uploaded = getattr(mapping, "uploaded_image", None)
            session_images.append(
                {
                    "image_id": str(uploaded.id) if uploaded else None,
                    "url": uploaded.public_url if uploaded else None,
                    "sequence_no": mapping.sequence_no,
                    "type": mapping.photo_type,
                }
            )
        
        serialized.append(
            {
                "session_id": str(session.id),
                "treatment_id": session.treatment_id,
                "date": session.treatment_date.isoformat() if session.treatment_date else None,
                "duration": session.duration_minutes,
                "is_completed": session.is_completed,
                "created_at": session.created_at.isoformat() if session.created_at else None,
                "images": session_images,
            }
        )
    return serialized

@router.post("/treatments", summary="고객별 시술 등록")
async def create_api_v1_treatments(
    request: treatment_request_11, 
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> treatment_response_11:
    """고객별 시술 등록 (로그인한 Shop의 고객만 시술 등록 가능)"""
    service = TreatmentService()
    request_dict = request.dict(exclude_unset=True)
    result = await service.create_treatment(db, request_dict, shop_id=current_shop.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Treatment creation failed"
        )
    return treatment_response_11(
        treatment_id=str(result.id),
        created_at=result.created_at.isoformat() if result.created_at else None
    )

@router.get("/treatments", summary="고객별 시술 목록")
async def list_api_v1_treatments(
    customer_id: Optional[int] = None,
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> treatment_response_12:
    """고객별 시술 목록 (로그인한 Shop의 고객 시술만 조회)"""
    service = TreatmentService()
    treatments = await service.list_treatments(db, customer_id=customer_id, shop_id=current_shop.id)
    
    treatments_list = []
    for t in treatments:
        sessions = _serialize_treatment_sessions(t)
        treatments_list.append(
            {
                "treatment_id": str(t.id),
                "customer_id": t.customer_id,
                "name": t.name,
                "type": t.type,
                "area": t.area,
                "is_completed": t.is_completed,
                "created_at": t.created_at.isoformat() if t.created_at else None,
                "sessions": sessions,
            }
        )
    
    return treatment_response_12(treatments=treatments_list)

@router.get("/treatments/{id}", summary="시술 상세")
async def get_api_v1_treatments_by_id(
    id: int = Path(..., description="시술 ID"),
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> treatment_response_13:
    """시술 상세 (로그인한 Shop의 시술만 조회 가능)"""
    service = TreatmentService()
    result = await service.get_treatment_by_id(db, id, shop_id=current_shop.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treatment not found"
        )
    sessions = _serialize_treatment_sessions(result)
    return treatment_response_13(
        treatment_id=str(result.id),
        customer_id=result.customer_id,
        name=result.name,
        type=result.type,
        area=result.area,
        is_completed=result.is_completed,
        created_at=result.created_at.isoformat() if result.created_at else None,
        updated_at=result.updated_at.isoformat() if result.updated_at else None,
        sessions=sessions,
    )

@router.put("/treatments/{id}", summary="시술 정보 수정")
async def update_api_v1_treatments_by_id(
    id: int = Path(..., description="시술 ID"),
    request: treatment_request_14 = ...,
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> treatment_response_14:
    """시술 정보 수정 (로그인한 Shop의 시술만 수정 가능)"""
    service = TreatmentService()
    request_dict = request.dict(exclude_unset=True)
    result = await service.update_treatment(db, id, request_dict, shop_id=current_shop.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treatment not found"
        )
    return treatment_response_14(
        updated_at=result.updated_at.isoformat() if result.updated_at else None
    )

@router.patch("/treatments/{id}/complete", summary="전체 회차 완료 시 완료처리")
async def patch_api_v1_treatments_by_id_complete(
    id: int = Path(..., description="시술 ID"),
    request: treatment_request_15 = ...,
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> treatment_response_15:
    """전체 회차 완료 시 완료처리 (로그인한 Shop의 시술만 완료 처리 가능)"""
    service = TreatmentService()
    if request.is_completed:
        success = await service.complete_treatment(db, id, shop_id=current_shop.id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot complete treatment: not all sessions are completed"
            )
    else:
        # Update is_completed directly
        request_dict = {"is_completed": False}
        result = await service.update_treatment(db, id, request_dict, shop_id=current_shop.id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Treatment not found"
            )
    
    return treatment_response_15(message="Treatment completion status updated successfully")

