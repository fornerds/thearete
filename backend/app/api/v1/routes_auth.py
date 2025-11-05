"""Authentication routes."""

import secrets
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import (
    get_current_user,
    revoke_token,
    store_token,
    is_token_revoked,
    get_user_sessions
)
from app.core.exceptions import (
    InvalidCredentialsException,
    TokenExpiredException,
    TokenInvalidException,
    UnauthorizedException,
    UserInactiveException
)
from app.core.security import create_tokens_with_expiry, verify_token, verify_password, create_shop_tokens
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.shop import Shop
from app.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
    LogoutRequest,
    TokenResponse,
    UserProfile,
    UserSessions,
    ShopLoginRequest,
    ShopLoginResponse,
    ShopLogoutRequest
)
from app.schemas.common import SuccessResponse
from app.services.user_service import UserService
from app.services.shop_service import ShopService
from app.core.auth import get_current_user, get_current_shop

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/user/login",
    response_model=TokenResponse,
    summary="User Login",
    description="Authenticate user and return access and refresh tokens",
    responses={
        200: {"description": "Login successful"},
        401: {"description": "Invalid credentials"},
        422: {"description": "Validation error"}
    }
)
async def user_login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    """User login endpoint with token management."""
    user_service = UserService()
    user = await user_service.get_user_by_email(db, login_data.email)
    
    if not user:
        raise InvalidCredentialsException("Invalid email or password")
    
    if not verify_password(login_data.password, user.hashed_password):
        raise InvalidCredentialsException("Invalid email or password")
    
    if not user.is_active:
        raise UserInactiveException("User account is disabled")
    
    # Create tokens with expiry information
    tokens = create_tokens_with_expiry(user.id, user.email)
    
    # Generate session ID
    session_id = f"sess_{secrets.token_urlsafe(16)}"
    
    # Store tokens in database
    access_expires = datetime.utcnow() + timedelta(minutes=30)  # 30 minutes
    refresh_expires = datetime.utcnow() + timedelta(days=7)     # 7 days
    
    await store_token(
        db=db,
        user_id=user.id,
        token=tokens["access_token"],
        token_type="access",
        expires_at=access_expires,
        device_info=login_data.device_info,
        session_id=session_id
    )
    
    await store_token(
        db=db,
        user_id=user.id,
        token=tokens["refresh_token"],
        token_type="refresh",
        expires_at=refresh_expires,
        device_info=login_data.device_info,
        session_id=session_id
    )
    
    return TokenResponse(**tokens)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh Access Token",
    description="Refresh access token using valid refresh token",
    responses={
        200: {"description": "Token refreshed successfully"},
        401: {"description": "Invalid or expired refresh token"},
        422: {"description": "Validation error"}
    }
)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    """Refresh access token endpoint."""
    # Verify refresh token
    payload = verify_token(refresh_data.refresh_token)
    
    if not payload:
        raise TokenInvalidException("Invalid refresh token")
    
    # Check token type
    if payload.get("type") != "refresh":
        raise TokenInvalidException("Invalid token type")
    
    # Check token expiration
    exp = payload.get("exp")
    if exp and datetime.utcnow().timestamp() > exp:
        raise TokenExpiredException("Refresh token has expired")
    
    # Check if token is revoked
    if await is_token_revoked(db, refresh_data.refresh_token):
        raise TokenInvalidException("Refresh token has been revoked")
    
    # Get user
    user_id = payload.get("sub")
    if not user_id:
        raise TokenInvalidException("Invalid token payload")
    
    user_service = UserService()
    user = await user_service.get_user_by_id(db, int(user_id))
    
    if not user:
        raise UnauthorizedException("User not found")
    
    if not user.is_active:
        raise UserInactiveException("User account is inactive")
    
    # Create new tokens
    tokens = create_tokens_with_expiry(user.id, user.email)
    
    # Store new tokens
    access_expires = datetime.utcnow() + timedelta(minutes=30)
    refresh_expires = datetime.utcnow() + timedelta(days=7)
    
    await store_token(
        db=db,
        user_id=user.id,
        token=tokens["access_token"],
        token_type="access",
        expires_at=access_expires
    )
    
    await store_token(
        db=db,
        user_id=user.id,
        token=tokens["refresh_token"],
        token_type="refresh",
        expires_at=refresh_expires
    )
    
    return TokenResponse(**tokens)


@router.post(
    "/logout",
    response_model=SuccessResponse,
    summary="User Logout",
    description="Logout user and revoke refresh token",
    responses={
        200: {"description": "Logout successful"},
        401: {"description": "Unauthorized"},
        422: {"description": "Validation error"}
    }
)
async def logout(
    logout_data: LogoutRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> SuccessResponse:
    """Logout endpoint with token revocation."""
    if logout_data.revoke_all:
        # Revoke all user tokens
        await revoke_token(db, "", revoke_all=True, user_id=current_user.id)
        message = "All sessions have been revoked"
    elif logout_data.refresh_token:
        # Revoke specific refresh token
        success = await revoke_token(db, logout_data.refresh_token)
        if not success:
            raise TokenInvalidException("Refresh token not found or already revoked")
        message = "Session has been revoked"
    else:
        # Just revoke current session (would need to track current session)
        message = "Logged out successfully"
    
    return SuccessResponse(message=message)


@router.get(
    "/me",
    response_model=UserProfile,
    summary="Get User Profile",
    description="Get current user profile information",
    responses={
        200: {"description": "User profile retrieved successfully"},
        401: {"description": "Unauthorized"}
    }
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
) -> UserProfile:
    """Get current user profile."""
    return UserProfile.from_orm(current_user)


@router.get(
    "/sessions",
    response_model=UserSessions,
    summary="Get User Sessions",
    description="Get all active user sessions",
    responses={
        200: {"description": "Sessions retrieved successfully"},
        401: {"description": "Unauthorized"}
    }
)
async def get_user_sessions_endpoint(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UserSessions:
    """Get user sessions."""
    sessions = await get_user_sessions(db, current_user.id)
    
    # Count active sessions
    active_sessions = sum(1 for session in sessions if session.is_valid)
    
    return UserSessions(
        active_sessions=active_sessions,
        sessions=sessions
    )


@router.post(
    "/revoke-session/{session_id}",
    response_model=SuccessResponse,
    summary="Revoke Specific Session",
    description="Revoke a specific user session",
    responses={
        200: {"description": "Session revoked successfully"},
        401: {"description": "Unauthorized"},
        404: {"description": "Session not found"}
    }
)
async def revoke_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> SuccessResponse:
    """Revoke a specific session."""
    from sqlalchemy import update
    from app.db.models.token import UserToken
    
    result = await db.execute(
        update(UserToken)
        .where(UserToken.session_id == session_id)
        .where(UserToken.user_id == current_user.id)
        .where(UserToken.is_revoked == False)
        .values(is_revoked=True, revoked_at=datetime.utcnow())
    )
    
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    await db.commit()
    
    return SuccessResponse(message="Session revoked successfully")


@router.post(
    "/login",
    response_model=ShopLoginResponse,
    summary="피부샵 로그인",
    description="Authenticate shop and return access and refresh tokens",
    responses={
        200: {"description": "Login successful"},
        401: {"description": "Invalid credentials"},
        422: {"description": "Validation error"}
    }
)
async def shop_login(
    login_data: ShopLoginRequest,
    db: AsyncSession = Depends(get_db)
) -> ShopLoginResponse:
    """Shop login endpoint (business login API)."""
    shop_service = ShopService()
    shop = await shop_service.get_shop_by_email(db, login_data.email)
    
    if not shop:
        raise InvalidCredentialsException("Invalid email or password")
    
    # Shop password가 None인 경우 처리
    if not shop.password:
        raise InvalidCredentialsException("Shop password not set. Please contact administrator.")
    
    # Shop password는 암호화되어 저장되어 있으므로 verify_password 사용
    if not verify_password(login_data.password, shop.password):
        raise InvalidCredentialsException("Invalid email or password")
    
    if shop.is_deleted:
        raise InvalidCredentialsException("Shop account is deleted")
    
    # Create tokens for shop
    tokens = create_shop_tokens(shop.id, shop.email)
    
    # Store refresh token in Shop model
    from sqlalchemy import update
    refresh_expires = datetime.utcnow() + timedelta(days=7)
    await db.execute(
        update(Shop)
        .where(Shop.id == shop.id)
        .values(
            refresh_token=tokens["refresh_token"],
            refresh_token_expiry=refresh_expires,
            last_login_at=datetime.utcnow()
        )
    )
    await db.commit()
    
    return ShopLoginResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        shop_id=shop.id
    )


@router.post(
    "/logout",
    response_model=SuccessResponse,
    summary="피부샵 로그아웃",
    description="Logout shop and revoke refresh token",
    responses={
        200: {"description": "Logout successful"},
        401: {"description": "Unauthorized"},
        422: {"description": "Validation error"}
    }
)
async def shop_logout(
    logout_data: ShopLogoutRequest,
    db: AsyncSession = Depends(get_db)
) -> SuccessResponse:
    """Shop logout endpoint."""
    # Verify refresh token
    payload = verify_token(logout_data.refresh_token)
    
    if not payload:
        raise TokenInvalidException("Invalid refresh token")
    
    # Check token type
    if payload.get("type") != "shop_refresh":
        raise TokenInvalidException("Invalid token type")
    
    # Get shop from token
    shop_id = payload.get("sub")
    if not shop_id:
        raise TokenInvalidException("Invalid token payload")
    
    shop_service = ShopService()
    shop = await shop_service.get_shop_by_id(db, int(shop_id))
    
    if not shop:
        raise UnauthorizedException("Shop not found")
    
    # Clear refresh token from Shop model
    from sqlalchemy import update
    result = await db.execute(
        update(Shop)
        .where(Shop.id == shop.id)
        .values(
            refresh_token=None,
            refresh_token_expiry=None
        )
    )
    await db.commit()
    
    return SuccessResponse(message="로그아웃 완료")
