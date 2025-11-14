"""FastAPI router for customer domain."""

from app.schemas.customer_request import Request6 as customer_request_6, Request7 as customer_request_7, Request8 as customer_request_8, Request9 as customer_request_9, Request10 as customer_request_10, Request11 as customer_request_11
from app.schemas.customer_response import Response6 as customer_response_6, Response7 as customer_response_7, Response8 as customer_response_8, Response9 as customer_response_9, Response10 as customer_response_10, Response11 as customer_response_11
from app.services.customer_service import CustomerService
from app.core.auth import get_current_shop
from app.db.models.shop import Shop
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from fastapi import Path
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

router = APIRouter(prefix="/v1", tags=["customer"])


def _format_customer_summary(customer) -> dict:
    """Format customer with treatment summaries."""
    from datetime import datetime
    
    treatments = [
        {
            "treatment_id": str(treatment.id),
            "type": treatment.type,
            "area": treatment.area,
            "is_completed": treatment.is_completed,
            "sessions": [
                {
                    "treatment_session_id": str(session.id),
                    "treatment_date": session.treatment_date.isoformat() if session.treatment_date else None,
                    "duration_minutes": session.duration_minutes,
                    "is_completed": session.is_completed,
                }
                for session in treatment.treatment_session
                if getattr(session, "is_deleted", False) is not True
            ],
        }
        for treatment in customer.treatment
        if getattr(treatment, "is_deleted", False) is not True
    ]
    
    # 최신 업데이트 시간 계산
    # 고객정보 생성/수정 시간, treatment 등록/수정시간, treatment session 등록/수정 중 가장 최신일시
    times = []
    if customer.created_at:
        times.append(customer.created_at)
    if customer.updated_at:
        times.append(customer.updated_at)
    # Treatment 시간
    for treatment in customer.treatment:
        if getattr(treatment, "is_deleted", False) is not True:
            if treatment.created_at:
                times.append(treatment.created_at)
            if treatment.updated_at:
                times.append(treatment.updated_at)
            # TreatmentSession 시간
            for session in treatment.treatment_session:
                if getattr(session, "is_deleted", False) is not True:
                    if session.created_at:
                        times.append(session.created_at)
                    if session.updated_at:
                        times.append(session.updated_at)
    
    latest_update_time = max(times).isoformat() if times else None
    
    return {
        "customer_id": str(customer.id),
        "name": customer.name,
        "gender": customer.gender,
        "age": customer.age,
        "skin_type": customer.skin_type,
        "marked": customer.marked,
        "latest_update_time": latest_update_time,
        "treatments": treatments,
    }

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
    sort: Optional[int] = Query(1, description="정렬 기준 (1: 최근 업데이트 순, 2: 최근 시술 순, 3: 고객명 순)"),
    order: Optional[str] = Query(None, description="정렬 방향 (asc: 오름차순, desc: 내림차순)"),
    search: Optional[str] = Query(None, description="고객명 검색 (LIKE 검색)"),
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> customer_response_7:
    """고객 리스트 (로그인한 Shop의 고객만 조회)
    
    정렬 기준:
    - 1: 최근 업데이트 순 (기본값: desc)
    - 2: 최근 시술 순 (기본값: desc)
    - 3: 고객명 가나다 순 (기본값: asc)
    """
    # sort_by 검증
    if sort not in [1, 2, 3]:
        sort = 1
    
    # sort_order가 제공되지 않으면 정렬 기준에 따라 기본값 설정
    if order is None:
        if sort == 3:
            order = "asc"  # 고객명은 기본 오름차순
        else:
            order = "desc"  # 업데이트/시술 순은 기본 내림차순
    
    # order 검증
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="order는 'asc' 또는 'desc'만 가능합니다."
        )
    
    service = CustomerService()
    result = await service.list_customers(
        db, 
        shop_id=current_shop.id,
        sort_by=sort,
        sort_order=order,
        search=search
    )
    customers = [_format_customer_summary(customer) for customer in result]
    return customer_response_7(customers=customers)

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
    summary = _format_customer_summary(result)
    return customer_response_8(**summary)

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

@router.patch("/customers/{id}/marked", summary="고객 상단 고정 토글/수정")
async def update_customer_marked(
    id: int = Path(..., description="고객 ID"), 
    request: Optional[customer_request_11] = Body(None),
    current_shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
) -> customer_response_11:
    """고객 상단 고정 상태 토글 또는 수정 (로그인한 Shop의 고객만 수정 가능)
    
    - marked가 None이면 현재 상태를 토글 (1 -> 0, 0 또는 None -> 1)
    - marked가 1이면 고정
    - marked가 0이면 해제
    """
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
    
    marked_value = request.marked if request else None
    result = await service.update_marked(db, id, marked_value)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return customer_response_11(
        customer_id=str(result.id),
        marked=result.marked,
        updated_at=result.updated_at.isoformat() if result.updated_at else None
    )

