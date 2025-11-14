"""Repository layer for customer domain."""

from app.db.models.customer import Customer
from app.db.models.treatment import Treatment
from app.db.models.treatment_session import TreatmentSession
from app.db.models.treatment_session_image import TreatmentSessionImage
from app.db.models.uploaded_image import UploadedImage
from sqlalchemy import select, update, delete, insert, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional, Any
from datetime import datetime

class CustomerRepository:
    """Repository for customer domain database operations."""
    
    async def get_by_id(self, db: AsyncSession, customer_id: int) -> Optional[Customer]:
        """Get customer by ID."""
        result = await db.execute(
            select(Customer)
            .options(
                selectinload(Customer.treatment)
                .selectinload(Treatment.treatment_session)
                .selectinload(TreatmentSession.images)
                .selectinload(TreatmentSessionImage.uploaded_image)
            )
            .where(Customer.id == customer_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(
        self, 
        db: AsyncSession, 
        shop_id: Optional[int] = None, 
        skip: int = 0, 
        limit: int = 100,
        sort_by: int = 1,
        sort_order: str = "desc",
        search: Optional[str] = None
    ) -> List[Customer]:
        """Get all customers with pagination, optionally filtered by shop_id, search term, and sorted."""
        query = (
            select(Customer)
            .options(
                selectinload(Customer.treatment)
                .selectinload(Treatment.treatment_session)
                .selectinload(TreatmentSession.images)
                .selectinload(TreatmentSessionImage.uploaded_image)
            )
        )
        if shop_id is not None:
            query = query.where(Customer.shop_id == shop_id)
        
        # is_deleted가 False이거나 None인 것만 필터링
        query = query.where(or_(Customer.is_deleted == False, Customer.is_deleted.is_(None)))
        
        # search 파라미터가 제공되면 고객명으로 LIKE 검색
        if search is not None and search.strip():
            query = query.where(Customer.name.ilike(f"%{search.strip()}%"))
        
        result = await db.execute(query)
        customers = result.scalars().all()
        
        # marked=1인 고객과 일반 고객 분리
        marked_customers = []
        normal_customers = []
        for customer in customers:
            if customer.marked == 1:
                marked_customers.append(customer)
            else:
                normal_customers.append(customer)
        
        # Python에서 정렬 처리 (복잡한 정렬 로직)
        try:
            if sort_by == 1:
                # 정렬 기준 1: 최근 업데이트 순
                # 고객정보 생성/수정 시간, treatment 등록/수정시간, treatment session 등록/수정 중 가장 최신일시
                def get_latest_update_time(customer: Customer) -> Optional[datetime]:
                    times = []
                    # 고객 정보 시간
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
                    return max(times) if times else None
                
                marked_customers = sorted(
                    marked_customers,
                    key=lambda c: (get_latest_update_time(c) or datetime.min),
                    reverse=(sort_order == "desc")
                )
                normal_customers = sorted(
                    normal_customers,
                    key=lambda c: (get_latest_update_time(c) or datetime.min),
                    reverse=(sort_order == "desc")
                )
                customers = marked_customers + normal_customers
            elif sort_by == 2:
                # 정렬 기준 2: 최근 시술 순
                # treatment_session 등록/수정시간 우선 비교, 다음으로 treatment 등록/수정 시간 비교
                # 시술 기록 없으면 가장 뒤로
                def get_latest_treatment_time(customer: Customer) -> Optional[datetime]:
                    times = []
                    # TreatmentSession 시간 우선
                    for treatment in customer.treatment:
                        if getattr(treatment, "is_deleted", False) is not True:
                            for session in treatment.treatment_session:
                                if getattr(session, "is_deleted", False) is not True:
                                    if session.created_at:
                                        times.append(session.created_at)
                                    if session.updated_at:
                                        times.append(session.updated_at)
                    # TreatmentSession이 없으면 Treatment 시간 사용
                    if not times:
                        for treatment in customer.treatment:
                            if getattr(treatment, "is_deleted", False) is not True:
                                if treatment.created_at:
                                    times.append(treatment.created_at)
                                if treatment.updated_at:
                                    times.append(treatment.updated_at)
                    return max(times) if times else None
                
                # 일반 고객: 시술 기록이 있는 고객과 없는 고객을 분리
                normal_with_treatment = []
                normal_without_treatment = []
                for customer in normal_customers:
                    latest_time = get_latest_treatment_time(customer)
                    if latest_time:
                        normal_with_treatment.append((customer, latest_time))
                    else:
                        normal_without_treatment.append(customer)
                
                # 시술 기록이 있는 고객 정렬
                normal_with_treatment.sort(
                    key=lambda x: x[1],
                    reverse=(sort_order == "desc")
                )
                
                # 시술 기록이 없는 고객은 항상 뒤로
                normal_sorted = [c for c, _ in normal_with_treatment] + normal_without_treatment
                
                # marked 고객도 같은 방식으로 정렬
                marked_with_treatment = []
                marked_without_treatment = []
                for customer in marked_customers:
                    latest_time = get_latest_treatment_time(customer)
                    if latest_time:
                        marked_with_treatment.append((customer, latest_time))
                    else:
                        marked_without_treatment.append(customer)
                
                marked_with_treatment.sort(
                    key=lambda x: x[1],
                    reverse=(sort_order == "desc")
                )
                marked_sorted = [c for c, _ in marked_with_treatment] + marked_without_treatment
                
                customers = marked_sorted + normal_sorted
            elif sort_by == 3:
                # 정렬 기준 3: 고객명 가나다 순
                def get_customer_name(customer: Customer) -> str:
                    return customer.name or ""
                
                marked_customers = sorted(
                    marked_customers,
                    key=get_customer_name,
                    reverse=(sort_order == "desc")
                )
                normal_customers = sorted(
                    normal_customers,
                    key=get_customer_name,
                    reverse=(sort_order == "desc")
                )
                customers = marked_customers + normal_customers
        except Exception as e:
            # 정렬 중 오류 발생 시 원본 리스트 반환
            import logging
            logging.error(f"Error sorting customers: {e}")
            pass
        
        # 페이지네이션 적용
        return customers[skip:skip + limit]
    
    async def create(self, db: AsyncSession, customer_data: dict) -> Customer:
        """Create new customer."""
        customer = Customer(**customer_data)
        db.add(customer)
        await db.commit()
        await db.refresh(customer)
        return customer
    
    async def get_by_shop_phone_name(
        self,
        db: AsyncSession,
        shop_id: int,
        phone: Optional[str],
        name: Optional[str],
    ) -> Optional[Customer]:
        """Get customer by shop, phone, and name combination."""
        result = await db.execute(
            select(Customer).where(
                and_(
                    Customer.shop_id == shop_id,
                    Customer.phone == phone,
                    Customer.name == name,
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def update(self, db: AsyncSession, customer_id: int, customer_data: dict) -> Optional[Customer]:
        """Update customer by ID."""
        result = await db.execute(
            update(Customer)
            .where(Customer.id == customer_id)
            .values(**customer_data)
        )
        await db.commit()
        
        if result.rowcount > 0:
            return await self.get_by_id(db, customer_id)
        return None
    
    async def delete(self, db: AsyncSession, customer_id: int) -> bool:
        """Delete customer by ID."""
        result = await db.execute(
            delete(Customer).where(Customer.id == customer_id)
        )
        await db.commit()
        return result.rowcount > 0
    
    async def update_marked(self, db: AsyncSession, customer_id: int, marked_value: Optional[int] = None) -> Optional[Customer]:
        """Update or toggle marked status for customer."""
        customer = await self.get_by_id(db, customer_id)
        if not customer:
            return None
        
        # marked_value가 None이면 toggle (1 -> 0, 0 또는 None -> 1)
        if marked_value is None:
            new_marked = 1 if (customer.marked is None or customer.marked == 0) else 0
        else:
            new_marked = marked_value
        
        # pinned(=marked) 변경 시 updated_at이 갱신되어 정렬 순서가 변하지 않도록 기존 값을 유지
        result = await db.execute(
            update(Customer)
            .where(Customer.id == customer_id)
            .values(marked=new_marked, updated_at=customer.updated_at)
        )
        await db.commit()
        
        if result.rowcount > 0:
            return await self.get_by_id(db, customer_id)
        return None



