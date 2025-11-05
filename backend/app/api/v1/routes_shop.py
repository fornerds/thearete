"""FastAPI router for shop domain."""

from app.schemas.shop_request import Request1 as shop_request_1, Request2 as shop_request_2, Request3 as shop_request_3, Request4 as shop_request_4, Request5 as shop_request_5
from app.schemas.shop_response import Response1 as shop_response_1, Response2 as shop_response_2, Response3 as shop_response_3, Response4 as shop_response_4, Response5 as shop_response_5
from app.services.shop_service import ShopService
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Path
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from datetime import datetime

router = APIRouter(prefix="/v1", tags=["shop"])

@router.post("/shops", summary="신규 피부샵 회원 등록")
async def create_api_v1_shops(request: shop_request_1, db: AsyncSession = Depends(get_db)) -> shop_response_1:
    """신규 피부샵 회원 등록"""
    # 비밀번호 유효성 검사 (추가 안전장치)
    if request.password:
        password_bytes = request.password.encode('utf-8')
        if len(password_bytes) > 72:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"비밀번호는 최대 72바이트까지 허용됩니다. 현재 비밀번호는 {len(password_bytes)}바이트입니다."
            )
    
    service = ShopService()
    request_dict = request.dict()
    # owner 필드를 owner_name으로 변환
    if "owner" in request_dict:
        request_dict["owner_name"] = request_dict.pop("owner")
    result = await service.create_shop(db, request_dict)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Shop creation failed"
        )
    return shop_response_1(shop_id=str(result.id), created_at=result.created_at.isoformat() if result.created_at else None)

@router.get("/shops", summary="전체 피부샵 목록")
async def list_api_v1_shops(db: AsyncSession = Depends(get_db)) -> List[shop_response_2]:
    """전체 피부샵 목록"""
    service = ShopService()
    result = await service.list_shops(db)
    # 빈 리스트도 정상 응답으로 반환
    if not result:
        return []
    # Shop 모델을 Response2 형식으로 변환
    return [
        shop_response_2(shop_id=str(shop.id), name=shop.name)
        for shop in result
    ]

@router.get("/shops/{id}", summary="특정 피부샵 상세")
async def get_api_v1_shops_by_id(id: int = Path(..., description="id ID"), db: AsyncSession = Depends(get_db)) -> shop_response_3:
    """특정 피부샵 상세"""
    service = ShopService()
    result = await service.get_shop_by_id(db, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shop not found"
        )
    # Shop 모델을 Response3 형식으로 변환
    return shop_response_3(
        shop_id=str(result.id),
        name=result.name,
        address=result.address,
        owner=result.owner_name
    )

@router.put("/shops/{id}", summary="피부샵 정보 수정")
async def update_api_v1_shops_by_id(request: shop_request_4, id: int = Path(..., description="id ID"), db: AsyncSession = Depends(get_db)) -> shop_response_4:
    """피부샵 정보 수정"""
    service = ShopService()
    result = await service.update_shop(db, id, request.dict())
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shop not found"
        )
    # Shop 모델을 Response4 형식으로 변환
    return shop_response_4(
        updated_at=result.updated_at.isoformat() if result.updated_at else None
    )

@router.delete("/shops/{id}", summary="삭제 여부 갱신")
async def delete_api_v1_shops_by_id(id: int = Path(..., description="id ID"), db: AsyncSession = Depends(get_db)) -> shop_response_5:
    """삭제 여부 갱신"""
    service = ShopService()
    result = await service.delete_shop(db, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shop not found"
        )
    # Response5 형식으로 변환
    return shop_response_5(deleted_at=datetime.utcnow().isoformat())

@router.get("/shop/summary", summary="Shop 요약")
async def list_api_v1_shop_summary(db: AsyncSession = Depends(get_db)):
    """GET /api/v1/shop/summary"""
    service = ShopService()
    result = await service.list_shops(db)
    # 빈 리스트도 정상 응답으로 반환
    return result if result is not None else []

