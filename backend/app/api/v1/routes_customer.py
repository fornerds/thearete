"""FastAPI router for customer domain."""

from app.schemas.customer_request import Request6 as customer_request_6, Request7 as customer_request_7, Request8 as customer_request_8, Request9 as customer_request_9, Request10 as customer_request_10
from app.schemas.customer_response import Response6 as customer_response_6, Response7 as customer_response_7, Response8 as customer_response_8, Response9 as customer_response_9, Response10 as customer_response_10
from app.services.customer_service import CustomerService
from app.core.auth import get_current_shop
from app.db.models.shop import Shop
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Path
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

router = APIRouter(prefix="/v1", tags=["customer"])

@router.post("/customers", summary="고객 프로필 등록")
async def create_api_v1_customers(
    request: customer_request_6, 
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> customer_response_6:
    """고객 프로필 등록 (로그인한 Shop에 속한 고객만 등록 가능)"""
    service = CustomerService()
    # 로그인한 Shop ID를 request에 추가
    request_dict = request.dict() if hasattr(request, 'dict') else request
    request_dict['shop_id'] = current_shop.id
    try:
        result = await service.create_customer(db, request_dict)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Customer creation failed"
        )
    return customer_response_6(
        customer_id=str(result.id),
        created_at=result.created_at.isoformat() if result.created_at else None
    )

@router.get("/customers", summary="고객 리스트")
async def list_api_v1_customers(
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> customer_response_7:
    """고객 리스트 (로그인한 Shop의 고객만 조회)"""
    service = CustomerService()
    result = await service.list_customers(db, shop_id=current_shop.id)
    # 빈 리스트도 정상 응답으로 반환
    if not result:
        return customer_response_7(customer_id=None, name=None)
    
    # Response7 스키마에 맞게 첫 번째 고객 반환 (스키마가 단일 객체 형태)
    if result:
        return customer_response_7(customer_id=str(result[0].id), name=result[0].name)
    return customer_response_7(customer_id=None, name=None)

@router.get("/customers/{id}", summary="고객 상세 정보")
async def get_api_v1_customers_by_id(
    id: int = Path(..., description="id ID"), 
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> customer_response_8:
    """고객 상세 정보 (로그인한 Shop의 고객만 조회 가능)"""
    service = CustomerService()
    result = await service.get_customer_by_id(db, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    # Shop ID 검증
    if result.shop_id != current_shop.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this customer"
        )
    return customer_response_8(
        customer_id=str(result.id),
        name=result.name,
        skin_type=result.skin_type
    )

@router.put("/customers/{id}", summary="고객 정보 수정")
async def update_api_v1_customers_by_id(
    request: customer_request_9, 
    id: int = Path(..., description="id ID"), 
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> customer_response_9:
    """고객 정보 수정 (로그인한 Shop의 고객만 수정 가능)"""
    service = CustomerService()
    # 먼저 고객이 현재 Shop에 속하는지 확인
    customer = await service.get_customer_by_id(db, id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    if customer.shop_id != current_shop.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this customer"
        )
    result = await service.update_customer(db, id, request)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer_response_9(
        updated_at=result.updated_at.isoformat() if result.updated_at else None
    )

@router.delete("/customers/{id}", summary="고객 비활성 처리")
async def delete_api_v1_customers_by_id(
    id: int = Path(..., description="id ID"), 
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> customer_response_10:
    """고객 비활성 처리 (로그인한 Shop의 고객만 삭제 가능)"""
    service = CustomerService()
    # 먼저 고객이 현재 Shop에 속하는지 확인
    customer = await service.get_customer_by_id(db, id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    if customer.shop_id != current_shop.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this customer"
        )
    result = await service.delete_customer(db, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return result

