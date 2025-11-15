"""Service layer for customer domain."""

from app.db.models.customer import Customer
from app.db.repositories.customer_repo import CustomerRepository
from app.schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any

class CustomerService:
    """Service for customer domain operations."""
    
    def __init__(self):
        self.repository = CustomerRepository()

    async def create_customer(self, db: AsyncSession, request_data) -> Customer:
        """Create new customer."""
        # Convert request to dict if it's a Pydantic model
        if hasattr(request_data, 'dict'):
            customer_dict = request_data.model_dump()
        else:
            customer_dict = request_data
        
        # Ensure age is an integer if provided
        if 'age' in customer_dict and customer_dict['age'] is not None:
            try:
                customer_dict['age'] = int(customer_dict['age'])
            except (ValueError, TypeError):
                customer_dict['age'] = None

        shop_id = customer_dict.get('shop_id')
        phone = customer_dict.get('phone')
        name = customer_dict.get('name')

        if shop_id is not None and phone is not None and name is not None:
            existing_customer = await self.repository.get_by_shop_phone_name(
                db=db,
                shop_id=shop_id,
                phone=phone,
                name=name,
            )
            if existing_customer:
                raise ValueError("동일한 이름과 연락처를 가진 고객이 이미 존재합니다.")
        
        return await self.repository.create(db, customer_dict)
    async def list_customers(
        self, 
        db: AsyncSession, 
        shop_id: Optional[int] = None, 
        skip: int = 0, 
        limit: int = 100,
        sort_by: int = 1,
        sort_order: str = "desc",
        search: Optional[str] = None
    ) -> List[Customer]:
        """List all customers, optionally filtered by shop_id, search term, and sorted."""
        return await self.repository.get_all(
            db, 
            shop_id=shop_id, 
            skip=skip, 
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            search=search
        )
    async def get_customer_by_id(self, db: AsyncSession, customer_id: int) -> Optional[Customer]:
        """Get customer by ID."""
        return await self.repository.get_by_id(db, customer_id)
    async def update_customer(self, db: AsyncSession, customer_id: int, request_data) -> Optional[Customer]:
        """Update customer by ID."""
        return await self.repository.update(db, customer_id, request_data.model_dump() if hasattr(request_data, 'dict') else request_data)
    async def delete_customer(self, db: AsyncSession, customer_id: int) -> bool:
        """Delete customer by ID."""
        return await self.repository.delete(db, customer_id)
    
    async def update_marked(self, db: AsyncSession, customer_id: int, marked_value: Optional[int] = None) -> Optional[Customer]:
        """Update or toggle marked status for customer."""
        return await self.repository.update_marked(db, customer_id, marked_value)

