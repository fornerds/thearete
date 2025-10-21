"""FastAPI router for shop domain."""

from app.schemas import *
from app.services.shop_service import ShopService
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Path
from typing import List, Optional

router = APIRouter(prefix="/v1/shop", tags=["shop"])

@router.post("/api/v1/shops")
@router.post("/api/v1/shops", summary="신규 피부샵 회원 등록")
async def create_api_v1_shops(request: shop_request_1) -> shop_response_1:
    """신규 피부샵 회원 등록"""
    service = ShopService()
    result = await service.create_shop(request)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shop not found"
        )
    return result

@router.get("/api/v1/shops")
@router.get("/api/v1/shops", summary="전체 피부샵 목록")
async def list_api_v1_shops(request: shop_request_2) -> shop_response_2:
    """전체 피부샵 목록"""
    service = ShopService()
    result = await service.list_shops()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shop not found"
        )
    return result

@router.get("/api/v1/shops/{id}")
@router.get("/api/v1/shops/{id}", summary="특정 피부샵 상세")
async def get_api_v1_shops_by_id(id: int = Path(..., description=f"id ID"), request: shop_request_3) -> shop_response_3:
    """특정 피부샵 상세"""
    service = ShopService()
    result = await service.get_shop_by_id(id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shop not found"
        )
    return result

@router.put("/api/v1/shops/{id}")
@router.put("/api/v1/shops/{id}", summary="피부샵 정보 수정")
async def update_api_v1_shops_by_id(id: int = Path(..., description=f"id ID"), request: shop_request_4) -> shop_response_4:
    """피부샵 정보 수정"""
    service = ShopService()
    result = await service.update_shop(id, request)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shop not found"
        )
    return result

@router.delete("/api/v1/shops/{id}")
@router.delete("/api/v1/shops/{id}", summary="삭제 여부 갱신")
async def delete_api_v1_shops_by_id(id: int = Path(..., description=f"id ID"), request: shop_request_5) -> shop_response_5:
    """삭제 여부 갱신"""
    service = ShopService()
    result = await service.delete_shop(id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shop not found"
        )
    return result

@router.get("/api/v1/shop/summary")
async def list_api_v1_shop_summary():
    """GET /api/v1/shop/summary"""
    service = ShopService()
    result = await service.list_shops()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shop not found"
        )
    return result

