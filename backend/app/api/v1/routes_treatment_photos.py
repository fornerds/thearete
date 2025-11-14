"""FastAPI router for treatment photos domain."""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_shop
from app.db.models.shop import Shop
from app.db.session import get_db
from app.schemas.treatment_photos_request import (
    Request27 as treatment_photos_request_27,
)
from app.schemas.treatment_photos_response import (
    Response27 as treatment_photos_response_27,
    Response29 as treatment_photos_response_29,
)
from app.services.treatment_photos_service import TreatmentPhotosService

router = APIRouter(prefix="/v1", tags=["treatment-photos"])


@router.post(
    "/treatment-photos",
    summary="전/후 사진 연결",
    response_model=treatment_photos_response_27,
)
async def create_api_v1_treatment_photos(
    request: treatment_photos_request_27,
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db),
) -> treatment_photos_response_27:
    """업로드된 이미지를 특정 시술 회차에 연결합니다."""
    service = TreatmentPhotosService()
    try:
        mappings = await service.attach_treatment_photos(
            db,
            treatment_id=request.treatment_id,
            session_id=request.session_id,
            images=[payload.dict() for payload in request.images],
            shop_id=current_shop.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return treatment_photos_response_27(
        photos=[
            {
                "photo_id": str(mapping.id),
                "treatment_id": mapping.treatment_id,
                "session_id": mapping.session_id,
                "type": mapping.photo_type,
                "image_url": mapping.uploaded_image.public_url if mapping.uploaded_image else None,
                "thumbnail_url": mapping.uploaded_image.thumbnail_url if mapping.uploaded_image else None,
                "created_at": mapping.created_at.isoformat() if mapping.created_at else None,
            }
            for mapping in mappings
        ]
    )


@router.get("/treatment-photos", summary="시술 사진 목록")
async def list_api_v1_treatment_photos(
    treatment_id: Optional[int] = None,
    session_id: Optional[int] = None,
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db),
):
    """시술 사진 목록 (로그인한 Shop의 사진만 조회)"""
    service = TreatmentPhotosService()
    mappings = await service.list_treatment_photos(
        db,
        treatment_id=treatment_id,
        session_id=session_id,
        shop_id=current_shop.id,
    )

    photos_list = [
        {
            "photo_id": str(mapping.id),
            "treatment_id": mapping.treatment_id,
            "session_id": mapping.session_id,
            "type": mapping.photo_type,
            "image_url": mapping.uploaded_image.public_url if mapping.uploaded_image else None,
            "thumbnail_url": mapping.uploaded_image.thumbnail_url if mapping.uploaded_image else None,
            "created_at": mapping.created_at.isoformat() if mapping.created_at else None,
        }
        for mapping in mappings
    ]

    return {"photos": photos_list}


@router.delete("/treatment-photos/{id}", summary="시술 사진 삭제")
async def delete_api_v1_treatment_photos_by_id(
    id: int = Path(..., description="사진 매핑 ID"),
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db),
) -> treatment_photos_response_29:
    """시술 사진 삭제 (로그인한 Shop의 사진만 삭제 가능)"""
    service = TreatmentPhotosService()
    success = await service.delete_treatment_photo(
        db,
        id,
        shop_id=current_shop.id,
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treatment photo not found",
        )
    return treatment_photos_response_29(
        deleted_at=datetime.utcnow().isoformat()
    )
