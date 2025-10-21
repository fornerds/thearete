"""User service for business logic."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException, NotFoundException
from app.core.security import get_password_hash, verify_password
from app.db.models.user import User
from app.db.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """User service for business logic."""
    
    def __init__(self, db: Optional[Session] = None):
        self.db = db
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        if not self.db:
            return None
        repo = UserRepository(self.db)
        return repo.get_user_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        if not self.db:
            return None
        repo = UserRepository(self.db)
        return repo.get_user_by_email(email)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        if not self.db:
            return None
        repo = UserRepository(self.db)
        return repo.get_user_by_username(username)
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users with pagination."""
        if not self.db:
            return []
        repo = UserRepository(self.db)
        return repo.get_users(skip=skip, limit=limit)
    
    def create_user(self, user_create: UserCreate) -> User:
        """Create a new user."""
        if not self.db:
            raise ValueError("Database session required")
        
        repo = UserRepository(self.db)
        
        # Check if user already exists
        if repo.get_user_by_email(user_create.email):
            raise ConflictException("User with this email already exists")
        
        if repo.get_user_by_username(user_create.username):
            raise ConflictException("User with this username already exists")
        
        # Hash password
        hashed_password = get_password_hash(user_create.password)
        
        # Create user data with hashed password
        user_data = user_create.model_copy()
        user_data.password = hashed_password
        
        return repo.create_user(user_data)
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        """Update user."""
        if not self.db:
            raise ValueError("Database session required")
        
        repo = UserRepository(self.db)
        
        # Check if user exists
        existing_user = repo.get_user_by_id(user_id)
        if not existing_user:
            raise NotFoundException("User not found")
        
        # Check for conflicts if updating email or username
        if user_update.email and user_update.email != existing_user.email:
            if repo.get_user_by_email(user_update.email):
                raise ConflictException("User with this email already exists")
        
        if user_update.username and user_update.username != existing_user.username:
            if repo.get_user_by_username(user_update.username):
                raise ConflictException("User with this username already exists")
        
        return repo.update_user(user_id, user_update)
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        if not self.db:
            raise ValueError("Database session required")
        
        repo = UserRepository(self.db)
        return repo.delete_user(user_id)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        user = self.get_user_by_email(email)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
