"""FastAPI router for customer domain."""

from app.schemas import *
from app.services.customer_service import CustomerService
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Path
from typing import List, Optional

router = APIRouter(prefix="/v1/customer", tags=["customer"])

@router.post("/api/v1/customers")
@router.post("/api/v1/customers", summary="고객 프로필 등록")
async def create_api_v1_customers(request: customer_request_6) -> customer_response_6:
    """고객 프로필 등록"""
    service = CustomerService()
    result = await service.create_customer(request)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return result

@router.get("/api/v1/customers")
@router.get("/api/v1/customers", summary="고객 리스트")
async def list_api_v1_customers(request: customer_request_7) -> customer_response_7:
    """고객 리스트"""
    service = CustomerService()
    result = await service.list_customers()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return result

@router.get("/api/v1/customers/{id}")
@router.get("/api/v1/customers/{id}", summary="고객 상세 정보")
async def get_api_v1_customers_by_id(id: int = Path(..., description=f"id ID"), request: customer_request_8) -> customer_response_8:
    """고객 상세 정보"""
    service = CustomerService()
    result = await service.get_customer_by_id(id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return result

@router.put("/api/v1/customers/{id}")
@router.put("/api/v1/customers/{id}", summary="고객 정보 수정")
async def update_api_v1_customers_by_id(id: int = Path(..., description=f"id ID"), request: customer_request_9) -> customer_response_9:
    """고객 정보 수정"""
    service = CustomerService()
    result = await service.update_customer(id, request)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return result

@router.delete("/api/v1/customers/{id}")
@router.delete("/api/v1/customers/{id}", summary="고객 비활성 처리")
async def delete_api_v1_customers_by_id(id: int = Path(..., description=f"id ID"), request: customer_request_10) -> customer_response_10:
    """고객 비활성 처리"""
    service = CustomerService()
    result = await service.delete_customer(id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return result

