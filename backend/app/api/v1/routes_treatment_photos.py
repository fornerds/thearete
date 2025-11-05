"""FastAPI router for treatment photos domain."""

from app.schemas.treatment_photos_request import Request27 as treatment_photos_request_27, Request28 as treatment_photos_request_28, Request29 as treatment_photos_request_29
from app.schemas.treatment_photos_response import Response27 as treatment_photos_response_27, Response28 as treatment_photos_response_28, Response29 as treatment_photos_response_29
from app.services.treatment_photos_service import TreatmentPhotosService
from app.core.auth import get_current_shop
from app.db.models.shop import Shop
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["treatment-photos"])

@router.post("/treatment-photos", summary="전/후 사진 등록")
async def create_api_v1_treatment_photos(
    request: treatment_photos_request_27,
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> treatment_photos_response_27:
    """전/후 사진 등록 (로그인한 Shop의 Treatment에만 사진 등록 가능)"""
    service = TreatmentPhotosService()
    request_dict = request.dict(exclude_unset=True)
    # Map type to photo_type
    if "type" in request_dict:
        request_dict["photo_type"] = request_dict.pop("type")
    # Map image_url to file_url
    if "image_url" in request_dict:
        request_dict["file_url"] = request_dict.pop("image_url")
    
    result = await service.create_treatment_photo(db, request_dict, shop_id=current_shop.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Treatment photo creation failed"
        )
    return treatment_photos_response_27(
        photo_id=str(result.id),
        created_at=result.created_at.isoformat() if result.created_at else None
    )

@router.get("/treatment-photos", summary="시술 사진 목록")
async def list_api_v1_treatment_photos(
    treatment_id: Optional[int] = None,
    session_id: Optional[int] = None,
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
):
    """시술 사진 목록 (로그인한 Shop의 사진만 조회)"""
    service = TreatmentPhotosService()
    photos = await service.list_treatment_photos(db, treatment_id=treatment_id, session_id=session_id, shop_id=current_shop.id)
    
    photos_list = [
        {
            "photo_id": str(p.id),
            "treatment_id": p.treatment_id,
            "session_id": p.session_id,
            "type": p.photo_type,
            "image_url": p.file_url,
            "created_at": p.created_at.isoformat() if p.created_at else None
        }
        for p in photos
    ]
    
    return {"photos": photos_list}

@router.delete("/treatment-photos/{id}", summary="시술 사진 삭제")
async def delete_api_v1_treatment_photos_by_id(
    id: int = Path(..., description="사진 ID"),
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> treatment_photos_response_29:
    """시술 사진 삭제 (로그인한 Shop의 사진만 삭제 가능)"""
    service = TreatmentPhotosService()
    success = await service.delete_treatment_photo(db, id, shop_id=current_shop.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treatment photo not found"
        )
    return treatment_photos_response_29(
        deleted_at=datetime.utcnow().isoformat()
    )
