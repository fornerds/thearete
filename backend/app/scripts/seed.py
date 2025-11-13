"""Database seeding script with comprehensive sample data."""

import asyncio
import logging
from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import get_password_hash
from app.db.session import AsyncSessionLocal
from app.db.models.user import User
from app.db.models.shop import Shop
from app.db.models.customer import Customer
from app.db.models.treatment import Treatment
from app.db.models.treatment_session import TreatmentSession
from app.db.models.skin_color_measurement import SkinColorMeasurement

logger = logging.getLogger(__name__)


async def create_admin_user(db: AsyncSession) -> User:
    """Create admin user."""
    # Check if admin user already exists
    result = await db.execute(select(User).where(User.email == "admin@thearete.com"))
    existing_admin = result.scalar_one_or_none()
    
    if existing_admin:
        logger.info("Admin user already exists, skipping creation")
        return existing_admin
    
    admin_user = User(
        email="admin@thearete.com",
        username="admin",
        hashed_password=get_password_hash("admin123!"),
        full_name="Thearete Admin",
        bio="System administrator for Thearete platform",
        is_active=True,
        is_superuser=True,
        avatar_url="https://example.com/admin-avatar.jpg"
    )
    
    db.add(admin_user)
    await db.commit()
    await db.refresh(admin_user)
    
    logger.info(f"Created admin user: {admin_user.email}")
    return admin_user


async def create_sample_users(db: AsyncSession) -> List[User]:
    """Create sample users."""
    # Check if users already exist
    result = await db.execute(select(User).where(User.is_superuser == False))
    existing_users = result.scalars().all()
    
    if existing_users:
        logger.info("Sample users already exist, skipping creation")
        return list(existing_users)
    
    users_data = [
        {
            "email": "shop.owner@thearete.com",
            "username": "shop_owner",
            "hashed_password": get_password_hash("shop123!"),
            "full_name": "김샵오너",
            "bio": "뷰티샵 운영자",
            "is_active": True,
            "is_superuser": False,
            "avatar_url": "https://example.com/shop-owner-avatar.jpg"
        },
        {
            "email": "customer1@thearete.com",
            "username": "customer1",
            "hashed_password": get_password_hash("customer123!"),
            "full_name": "이고객",
            "bio": "뷰티 서비스 이용 고객",
            "is_active": True,
            "is_superuser": False,
            "avatar_url": "https://example.com/customer1-avatar.jpg"
        },
        {
            "email": "customer2@thearete.com",
            "username": "customer2",
            "hashed_password": get_password_hash("customer123!"),
            "full_name": "박고객",
            "bio": "뷰티 서비스 이용 고객",
            "is_active": True,
            "is_superuser": False,
            "avatar_url": "https://example.com/customer2-avatar.jpg"
        },
        {
            "email": "therapist@thearete.com",
            "username": "therapist",
            "hashed_password": get_password_hash("therapist123!"),
            "full_name": "최테라피스트",
            "bio": "전문 뷰티 테라피스트",
            "is_active": True,
            "is_superuser": False,
            "avatar_url": "https://example.com/therapist-avatar.jpg"
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User(**user_data)
        db.add(user)
        users.append(user)
    
    await db.commit()
    
    # Refresh all users to get IDs
    for user in users:
        await db.refresh(user)
    
    logger.info(f"Created {len(users)} sample users")
    return users


async def create_sample_shops(db: AsyncSession, shop_owner: User) -> List[Shop]:
    """Create sample shops."""
    # Check if shops already exist
    result = await db.execute(select(Shop))
    existing_shops = result.scalars().all()
    
    if existing_shops:
        logger.info("Sample shops already exist, skipping creation")
        return list(existing_shops)
    
    shops_data = [
        {
            "name": "뷰티샵 서울점",
            "address": "서울시 강남구 테헤란로 123",
            "owner_name": "김샵오너",
            "phone": "02-1234-5678",
            "email": "seoul@beautyshop.com",
            "password": get_password_hash("shop123!"),
            "is_deleted": False
        },
        {
            "name": "뷰티샵 부산점",
            "address": "부산시 해운대구 해운대로 456",
            "owner_name": "김샵오너",
            "phone": "051-2345-6789",
            "email": "busan@beautyshop.com",
            "password": get_password_hash("shop123!"),
            "is_deleted": False
        }
    ]
    
    shops = []
    for shop_data in shops_data:
        shop = Shop(**shop_data)
        db.add(shop)
        shops.append(shop)
    
    await db.commit()
    
    # Refresh all shops to get IDs
    for shop in shops:
        await db.refresh(shop)
    
    logger.info(f"Created {len(shops)} sample shops")
    return shops


async def create_sample_customers(db: AsyncSession, shops: List[Shop]) -> List[Customer]:
    """Create sample customers."""
    # Check if customers already exist
    result = await db.execute(select(Customer))
    existing_customers = result.scalars().all()
    
    if existing_customers:
        logger.info("Sample customers already exist, skipping creation")
        return list(existing_customers)
    
    customers = []
    for i, shop in enumerate(shops):
        customer = Customer(
            shop_id=shop.id,
            name=f"고객{i+1}",
            age=25 + i,
            gender="F",
            phone=f"010-1234-567{i}",
            skin_type="combination",
            note=f"{shop.name}의 고객{i+1}",
            marked=0,
            is_deleted=False
        )
        db.add(customer)
        customers.append(customer)
    
    await db.commit()
    
    # Refresh all customers to get IDs
    for customer in customers:
        await db.refresh(customer)
    
    logger.info(f"Created {len(customers)} sample customers")
    return customers


async def create_sample_treatments(db: AsyncSession, shops: List[Shop]) -> List[Treatment]:
    """Create sample treatments."""
    # Check if treatments already exist
    result = await db.execute(select(Treatment))
    existing_treatments = result.scalars().all()
    
    if existing_treatments:
        logger.info("Sample treatments already exist, skipping creation")
        return list(existing_treatments)
    
    treatments = []
    for shop in shops:
        shop_treatments = [
            {
                "name": "기본 피부관리",
                "description": "기본적인 클렌징과 보습 관리",
                "duration_minutes": 60,
                "price": 50000,
                "shop_id": shop.id,
                "is_active": True,
                "category": "피부관리",
                "difficulty_level": "beginner"
            },
            {
                "name": "프리미엄 피부관리",
                "description": "고급 장비를 사용한 전문 피부관리",
                "duration_minutes": 90,
                "price": 100000,
                "shop_id": shop.id,
                "is_active": True,
                "category": "피부관리",
                "difficulty_level": "advanced"
            },
            {
                "name": "메이크업 서비스",
                "description": "데일리 메이크업 서비스",
                "duration_minutes": 45,
                "price": 30000,
                "shop_id": shop.id,
                "is_active": True,
                "category": "메이크업",
                "difficulty_level": "intermediate"
            }
        ]
        
        for treatment_data in shop_treatments:
            treatment = Treatment(**treatment_data)
            db.add(treatment)
            treatments.append(treatment)
    
    await db.commit()
    
    # Refresh all treatments to get IDs
    for treatment in treatments:
        await db.refresh(treatment)
    
    logger.info(f"Created {len(treatments)} sample treatments")
    return treatments


async def create_sample_treatment_sessions(
    db: AsyncSession, 
    customers: List[Customer], 
    treatments: List[Treatment]
) -> List[TreatmentSession]:
    """Create sample treatment sessions."""
    # Check if treatment sessions already exist
    result = await db.execute(select(TreatmentSession))
    existing_sessions = result.scalars().all()
    
    if existing_sessions:
        logger.info("Sample treatment sessions already exist, skipping creation")
        return list(existing_sessions)
    
    sessions = []
    for i, customer in enumerate(customers):
        # Each customer gets 2-3 sessions
        for j in range(2):
            treatment = treatments[i % len(treatments)]
            session = TreatmentSession(
                customer_id=customer.id,
                treatment_id=treatment.id,
                scheduled_at=datetime(2024, 1, 15 + j, 14 + j, 0),
                status="completed",
                notes=f"{customer.user.full_name}의 {treatment.name} 세션",
                therapist_notes=f"고객 만족도 높음, 재방문 희망",
                rating=4.5,
                feedback="서비스가 매우 만족스러웠습니다."
            )
            db.add(session)
            sessions.append(session)
    
    await db.commit()
    
    # Refresh all sessions to get IDs
    for session in sessions:
        await db.refresh(session)
    
    logger.info(f"Created {len(sessions)} sample treatment sessions")
    return sessions


async def create_sample_skin_measurements(
    db: AsyncSession, 
    customers: List[Customer]
) -> List[SkinColorMeasurement]:
    """Create sample skin color measurements."""
    # Check if measurements already exist
    result = await db.execute(select(SkinColorMeasurement))
    existing_measurements = result.scalars().all()
    
    if existing_measurements:
        logger.info("Sample skin measurements already exist, skipping creation")
        return list(existing_measurements)
    
    measurements = []
    for customer in customers:
        measurement = SkinColorMeasurement(
            customer_id=customer.id,
            measurement_date=datetime(2024, 1, 10),
            l_value=65.5,
            a_value=12.3,
            b_value=18.7,
            skin_tone="light-medium",
            undertone="warm",
            notes=f"{customer.user.full_name}의 피부톤 측정 결과"
        )
        db.add(measurement)
        measurements.append(measurement)
    
    await db.commit()
    
    # Refresh all measurements to get IDs
    for measurement in measurements:
        await db.refresh(measurement)
    
    logger.info(f"Created {len(measurements)} sample skin measurements")
    return measurements


async def seed_database() -> None:
    """Seed the database with comprehensive sample data."""
    async with AsyncSessionLocal() as db:
        try:
            logger.info("Starting comprehensive database seeding...")
            
            # Create admin user
            admin_user = await create_admin_user(db)
            
            # Create sample users
            users = await create_sample_users(db)
            all_users = [admin_user] + users
            
            # Create sample shops
            shops = await create_sample_shops(db, admin_user)
            
            # Create sample customers
            customers = await create_sample_customers(db, shops)
            
            logger.info("Database seeding completed successfully!")
            logger.info(f"Created: {len(all_users)} users, {len(shops)} shops, "
                       f"{len(customers)} customers")
            
        except Exception as e:
            logger.error(f"Error seeding database: {e}")
            await db.rollback()
            raise


async def main():
    """Main function for running seed script."""
    await seed_database()


if __name__ == "__main__":
    asyncio.run(main())
