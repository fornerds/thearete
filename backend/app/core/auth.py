"""Authentication utilities and OAuth2 scheme."""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    TokenExpiredException,
    TokenInvalidException,
    UnauthorizedException,
    UserInactiveException,
    ForbiddenException
)
from app.core.security import verify_token, create_access_token, create_refresh_token
from app.db.models.user import User
from app.db.models.token import UserToken
from app.db.models.shop import Shop
from app.db.session import get_db
from app.services.user_service import UserService
from app.services.shop_service import ShopService

# OAuth2 scheme
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token."""
    if not credentials:
        raise UnauthorizedException("Not authenticated")
    
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise TokenInvalidException("Invalid authentication credentials")
    
    # Check token type
    if payload.get("type") != "access":
        raise TokenInvalidException("Invalid token type")
    
    # Check token expiration
    exp = payload.get("exp")
    if exp and datetime.utcnow().timestamp() > exp:
        raise TokenExpiredException("Token has expired")
    
    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise TokenInvalidException("Invalid token payload")
    
    # Get user from database
    user_service = UserService()
    user = await user_service.get_user_by_id(db, int(user_id))
    
    if user is None:
        raise UnauthorizedException("User not found")
    
    if not user.is_active:
        raise UserInactiveException("User account is inactive")
    
    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """Get current user if authenticated, otherwise None."""
    try:
        return await get_current_user(credentials, db)
    except (UnauthorizedException, TokenExpiredException, TokenInvalidException, UserInactiveException):
        return None


def require_scopes(*required_scopes: str):
    """Decorator to require specific scopes/permissions."""
    async def scope_checker(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ) -> User:
        # Get user scopes from database or user attributes
        user_scopes = await get_user_scopes(current_user, db)
        
        if not all(scope in user_scopes for scope in required_scopes):
            raise ForbiddenException("Insufficient permissions")
        
        return current_user
    
    return scope_checker


async def get_user_scopes(user: User, db: AsyncSession) -> List[str]:
    """Get user scopes/permissions."""
    scopes = []
    
    # Basic user scope
    scopes.append("user")
    
    # Admin scope for superusers
    if user.is_superuser:
        scopes.append("admin")
    
    # Add more scope logic based on user roles, groups, etc.
    # This can be extended based on your business requirements
    
    return scopes


def hash_token(token: str) -> str:
    """Hash token for storage in database."""
    return hashlib.sha256(token.encode()).hexdigest()


async def store_token(
    db: AsyncSession,
    user_id: int,
    token: str,
    token_type: str,
    expires_at: datetime,
    device_info: Optional[str] = None,
    session_id: Optional[str] = None
) -> UserToken:
    """Store token in database."""
    token_hash = hash_token(token)
    
    user_token = UserToken(
        user_id=user_id,
        token_hash=token_hash,
        token_type=token_type,
        expires_at=expires_at,
        device_info=device_info,
        session_id=session_id
    )
    
    db.add(user_token)
    await db.commit()
    await db.refresh(user_token)
    
    return user_token


async def revoke_token(
    db: AsyncSession,
    token: str,
    revoke_all: bool = False,
    user_id: Optional[int] = None
) -> bool:
    """Revoke token(s) in database."""
    token_hash = hash_token(token)
    
    if revoke_all and user_id:
        # Revoke all user tokens
        from sqlalchemy import update
        await db.execute(
            update(UserToken)
            .where(UserToken.user_id == user_id)
            .where(UserToken.is_revoked == False)
            .values(is_revoked=True, revoked_at=datetime.utcnow())
        )
    else:
        # Revoke specific token
        from sqlalchemy import update
        result = await db.execute(
            update(UserToken)
            .where(UserToken.token_hash == token_hash)
            .where(UserToken.is_revoked == False)
            .values(is_revoked=True, revoked_at=datetime.utcnow())
        )
        
        if result.rowcount == 0:
            return False
    
    await db.commit()
    return True


async def is_token_revoked(db: AsyncSession, token: str) -> bool:
    """Check if token is revoked."""
    token_hash = hash_token(token)
    
    from sqlalchemy import select
    result = await db.execute(
        select(UserToken)
        .where(UserToken.token_hash == token_hash)
        .where(UserToken.is_revoked == True)
    )
    
    return result.scalar_one_or_none() is not None


async def cleanup_expired_tokens(db: AsyncSession) -> int:
    """Clean up expired tokens from database."""
    from sqlalchemy import delete
    result = await db.execute(
        delete(UserToken)
        .where(UserToken.expires_at < datetime.utcnow())
    )
    
    await db.commit()
    return result.rowcount


async def get_user_sessions(db: AsyncSession, user_id: int) -> List[UserToken]:
    """Get all user sessions."""
    from sqlalchemy import select
    result = await db.execute(
        select(UserToken)
        .where(UserToken.user_id == user_id)
        .where(UserToken.token_type == "refresh")
        .order_by(UserToken.created_at.desc())
    )
    
    return result.scalars().all()


# Scope-based dependencies
require_admin = require_scopes("admin")
require_user = require_scopes("user")


async def get_current_shop(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Shop:
    """Get current authenticated shop from JWT token."""
    if not credentials:
        raise UnauthorizedException("Not authenticated")
    
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise TokenInvalidException("Invalid authentication credentials")
    
    # Check token type - Shop tokens use "shop_access" type
    if payload.get("type") != "shop_access":
        raise TokenInvalidException("Invalid token type")
    
    # Check token expiration
    exp = payload.get("exp")
    if exp and datetime.utcnow().timestamp() > exp:
        raise TokenExpiredException("Token has expired")
    
    shop_id: Optional[str] = payload.get("sub")
    if shop_id is None:
        raise TokenInvalidException("Invalid token payload")
    
    # Get shop from database
    shop_service = ShopService()
    shop = await shop_service.get_shop_by_id(db, int(shop_id))
    
    if shop is None:
        raise UnauthorizedException("Shop not found")
    
    if shop.is_deleted:
        raise UnauthorizedException("Shop is deleted")
    
    return shop
