"""Dependency injection for FastAPI routes."""

from typing import Annotated, Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.security import verify_token
from app.db.session import get_db
from app.schemas.user import User


# Database dependency
def get_database() -> Generator[Session, None, None]:
    """Get database session."""
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


# Current user dependency
def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


# Optional current user dependency
def get_current_user_optional(
    token: Annotated[str, Depends(verify_token)]
) -> User | None:
    """Get current user if authenticated, otherwise None."""
    if not token:
        return None
    return get_current_user(token)


# Type aliases for common dependencies
DatabaseDep = Annotated[Session, Depends(get_database)]
CurrentUserDep = Annotated[User, Depends(get_current_active_user)]
OptionalUserDep = Annotated[User | None, Depends(get_current_user_optional)]
