"""User repository for database operations."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    """User repository for database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users with pagination."""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def create_user(self, user: UserCreate) -> User:
        """Create a new user."""
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=user.password,  # This should be hashed in service layer
            full_name=user.full_name,
            bio=user.bio,
            avatar_url=user.avatar_url,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user."""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        return True
