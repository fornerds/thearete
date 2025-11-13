"""FastAPI router for upload operations."""

from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.auth import get_current_shop
from app.db.models.shop import Shop
from app.db.session import get_db
from app.db.repositories.uploaded_image_repo import UploadedImageRepository
from app.schemas.uploads_response import UploadImagesResponse, UploadedImageItem
from app.services.upload_service import UploadService

router = APIRouter(prefix="/api/v1/uploads", tags=["uploads"])

# 동적으로 다운로드 라우터 생성: UPLOAD_URL_PREFIX 설정값 사용
# prefix에서 앞의 슬래시 제거 (예: "/uploads" -> "uploads")
_upload_url_prefix = settings.upload_url_prefix.lstrip("/")
download_router = APIRouter(prefix=f"/{_upload_url_prefix}", tags=["uploads"])


@router.post(
    "/images",
    summary="이미지 업로드",
    response_model=UploadImagesResponse,
)
async def upload_images(
    files: List[UploadFile] = File(..., description="업로드할 이미지 파일 리스트"),
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db),
) -> UploadImagesResponse:
    """이미지를 업로드하고 접근 가능한 URL을 반환합니다."""
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="업로드할 파일을 한 개 이상 선택해주세요.",
        )

    service = UploadService()
    try:
        records = await service.upload_images(db, files)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"파일 업로드 실패: {exc}",
        ) from exc

    return UploadImagesResponse(
        uploads=[
            UploadedImageItem(
                image_id=str(record.id),
                url=record.public_url,
                original_filename=record.original_filename,
            )
            for record in records
        ]
    )


@download_router.get(
    "/{image_path:path}",
    summary="이미지 다운로드 (인증 필요)",
    response_class=Response,
)
async def download_image(
    image_path: str,
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db),
) -> Response:
    """이미지 다운로드 엔드포인트. 인증된 shop이 treatment_session에 연결된 이미지만 접근 가능."""
    # public_url 형식: {UPLOAD_URL_PREFIX}/images/{filename}
    # image_path는 이미 "images/{filename}" 형식
    # UPLOAD_URL_PREFIX 설정값을 사용하여 full_url 생성
    upload_prefix = settings.upload_url_prefix.rstrip("/")
    if not upload_prefix.startswith("/"):
        upload_prefix = f"/{upload_prefix}"
    full_url = f"{upload_prefix}/{image_path}"
    
    # public_url로 이미지 찾기
    repository = UploadedImageRepository()
    image = await repository.get_by_url_with_shop_check(
        db,
        url=full_url,
        shop_id=current_shop.id,
    )
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="이미지를 찾을 수 없거나 접근 권한이 없습니다.",
        )
    
    # X-Accel-Redirect 헤더 설정
    # Nginx의 internal location으로 전달할 경로
    # storage_path는 이미 "images/filename.jpg" 형식
    internal_path = f"/_protected/{image.storage_path}"
    
    response = Response(status_code=200)
    response.headers["X-Accel-Redirect"] = internal_path
    response.headers["Content-Type"] = image.content_type or "application/octet-stream"
    response.headers["Cache-Control"] = "private, max-age=600"
    
    return response

