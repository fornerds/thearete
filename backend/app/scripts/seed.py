"""Database seeding script."""

import asyncio
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.db.models.user import User
from app.db.models.item import Item


def create_sample_users(db: Session) -> None:
    """Create sample users."""
    # Check if users already exist
    if db.query(User).first():
        print("Users already exist, skipping user creation")
        return
    
    users_data = [
        {
            "email": "admin@example.com",
            "username": "admin",
            "hashed_password": get_password_hash("admin123"),
            "full_name": "Admin User",
            "bio": "System administrator",
            "is_superuser": True,
        },
        {
            "email": "user1@example.com",
            "username": "user1",
            "hashed_password": get_password_hash("user123"),
            "full_name": "John Doe",
            "bio": "Regular user",
            "is_superuser": False,
        },
        {
            "email": "user2@example.com",
            "username": "user2",
            "hashed_password": get_password_hash("user123"),
            "full_name": "Jane Smith",
            "bio": "Another regular user",
            "is_superuser": False,
        },
    ]
    
    for user_data in users_data:
        user = User(**user_data)
        db.add(user)
    
    db.commit()
    print("Created sample users")


def create_sample_items(db: Session) -> None:
    """Create sample items."""
    # Check if items already exist
    if db.query(Item).first():
        print("Items already exist, skipping item creation")
        return
    
    # Get users
    users = db.query(User).all()
    if not users:
        print("No users found, cannot create items")
        return
    
    items_data = [
        {
            "title": "Sample Item 1",
            "description": "This is a sample item for testing",
            "price": 29.99,
            "owner_id": users[0].id,
        },
        {
            "title": "Sample Item 2",
            "description": "Another sample item",
            "price": 49.99,
            "owner_id": users[1].id,
        },
        {
            "title": "Free Item",
            "description": "This item is free",
            "price": 0.0,
            "owner_id": users[2].id,
        },
    ]
    
    for item_data in items_data:
        item = Item(**item_data)
        db.add(item)
    
    db.commit()
    print("Created sample items")


def seed_database() -> None:
    """Seed the database with sample data."""
    db = SessionLocal()
    try:
        print("Starting database seeding...")
        create_sample_users(db)
        create_sample_items(db)
        print("Database seeding completed successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
