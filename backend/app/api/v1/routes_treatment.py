"""FastAPI router for treatment domain."""

from app.schemas.treatment_request import Request11 as treatment_request_11, Request12 as treatment_request_12, Request13 as treatment_request_13, Request14 as treatment_request_14, Request15 as treatment_request_15
from app.schemas.treatment_response import Response11 as treatment_response_11, Response12 as treatment_response_12, Response13 as treatment_response_13, Response14 as treatment_response_14, Response15 as treatment_response_15
from app.services.treatment_service import TreatmentService
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from typing import List, Optional

router = APIRouter(prefix="/api/v1", tags=["treatment"])

@router.post("/treatments", summary="고객별 시술 등록")
async def create_api_v1_treatments(
    request: treatment_request_11, 
    db: AsyncSession = Depends(get_db)
) -> treatment_response_11:
    """고객별 시술 등록"""
    service = TreatmentService()
    request_dict = request.dict(exclude_unset=True)
    result = await service.create_treatment(db, request_dict)
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
    db: AsyncSession = Depends(get_db)
) -> treatment_response_12:
    """고객별 시술 목록"""
    service = TreatmentService()
    treatments = await service.list_treatments(db, customer_id=customer_id)
    
    treatments_list = [
        {
            "treatment_id": str(t.id),
            "customer_id": t.customer_id,
            "type": t.type,
            "area": t.area,
            "is_completed": t.is_completed,
            "created_at": t.created_at.isoformat() if t.created_at else None
        }
        for t in treatments
    ]
    
    return treatment_response_12(treatments=treatments_list)

@router.get("/treatments/{id}", summary="시술 상세")
async def get_api_v1_treatments_by_id(
    id: int = Path(..., description="시술 ID"),
    db: AsyncSession = Depends(get_db)
) -> treatment_response_13:
    """시술 상세"""
    service = TreatmentService()
    result = await service.get_treatment_by_id(db, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treatment not found"
        )
    return treatment_response_13(
        treatment_id=str(result.id),
        customer_id=result.customer_id,
        type=result.type,
        area=result.area,
        is_completed=result.is_completed,
        created_at=result.created_at.isoformat() if result.created_at else None,
        updated_at=result.updated_at.isoformat() if result.updated_at else None
    )

@router.put("/treatments/{id}", summary="시술 정보 수정")
async def update_api_v1_treatments_by_id(
    id: int = Path(..., description="시술 ID"),
    request: treatment_request_14 = ...,
    db: AsyncSession = Depends(get_db)
) -> treatment_response_14:
    """시술 정보 수정"""
    service = TreatmentService()
    request_dict = request.dict(exclude_unset=True)
    result = await service.update_treatment(db, id, request_dict)
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
    db: AsyncSession = Depends(get_db)
) -> treatment_response_15:
    """전체 회차 완료 시 완료처리"""
    service = TreatmentService()
    if request.is_completed:
        success = await service.complete_treatment(db, id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot complete treatment: not all sessions are completed"
            )
    else:
        # Update is_completed directly
        request_dict = {"is_completed": False}
        result = await service.update_treatment(db, id, request_dict)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Treatment not found"
            )
    
    return treatment_response_15(message="Treatment completion status updated successfully")

