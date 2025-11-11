"""Repository layer for customer domain."""

from app.db.models.customer import Customer
from app.db.models.treatment import Treatment
from sqlalchemy import select, update, delete, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional, Any

class CustomerRepository:
    """Repository for customer domain database operations."""
    
    async def get_by_id(self, db: AsyncSession, customer_id: int) -> Optional[Customer]:
        """Get customer by ID."""
        result = await db.execute(
            select(Customer)
            .options(
                selectinload(Customer.treatment).selectinload(Treatment.treatment_session)
            )
            .where(Customer.id == customer_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, db: AsyncSession, shop_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Customer]:
        """Get all customers with pagination, optionally filtered by shop_id."""
        query = (
            select(Customer)
            .options(
                selectinload(Customer.treatment).selectinload(Treatment.treatment_session)
            )
        )
        if shop_id is not None:
            query = query.where(Customer.shop_id == shop_id)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
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



