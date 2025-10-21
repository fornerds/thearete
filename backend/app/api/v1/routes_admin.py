"""Admin-only routes for testing scope-based access control."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user, require_admin, require_user
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.common import SuccessResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get(
    "/users",
    response_model=SuccessResponse,
    summary="List All Users",
    description="Admin-only endpoint to list all users",
    responses={
        200: {"description": "Users retrieved successfully"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden - Admin access required"}
    }
)
async def list_all_users(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
) -> SuccessResponse:
    """List all users - Admin only."""
    from app.services.user_service import UserService
    
    user_service = UserService()
    users = await user_service.get_all_users(db)
    
    # Convert to dict for JSON serialization
    users_data = [
        {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "created_at": user.created_at.isoformat()
        }
        for user in users
    ]
    
    return SuccessResponse(
        message=f"Retrieved {len(users_data)} users",
        data={"users": users_data}
    )


@router.get(
    "/stats",
    response_model=SuccessResponse,
    summary="System Statistics",
    description="Admin-only endpoint for system statistics",
    responses={
        200: {"description": "Statistics retrieved successfully"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden - Admin access required"}
    }
)
async def get_system_stats(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
) -> SuccessResponse:
    """Get system statistics - Admin only."""
    from sqlalchemy import select, func
    from app.db.models.user import User
    from app.db.models.token import UserToken
    
    # Count total users
    user_count_result = await db.execute(select(func.count(User.id)))
    user_count = user_count_result.scalar()
    
    # Count active users
    active_user_count_result = await db.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )
    active_user_count = active_user_count_result.scalar()
    
    # Count admin users
    admin_count_result = await db.execute(
        select(func.count(User.id)).where(User.is_superuser == True)
    )
    admin_count = admin_count_result.scalar()
    
    # Count active tokens
    active_token_count_result = await db.execute(
        select(func.count(UserToken.id))
        .where(UserToken.is_revoked == False)
        .where(UserToken.expires_at > func.now())
    )
    active_token_count = active_token_count_result.scalar()
    
    stats = {
        "total_users": user_count,
        "active_users": active_user_count,
        "admin_users": admin_count,
        "active_tokens": active_token_count,
        "inactive_users": user_count - active_user_count
    }
    
    return SuccessResponse(
        message="System statistics retrieved successfully",
        data=stats
    )


@router.post(
    "/users/{user_id}/activate",
    response_model=SuccessResponse,
    summary="Activate User",
    description="Admin-only endpoint to activate a user account",
    responses={
        200: {"description": "User activated successfully"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden - Admin access required"},
        404: {"description": "User not found"}
    }
)
async def activate_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
) -> SuccessResponse:
    """Activate a user account - Admin only."""
    from app.services.user_service import UserService
    from sqlalchemy import update
    
    user_service = UserService()
    user = await user_service.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_active:
        return SuccessResponse(message="User is already active")
    
    # Activate user
    await db.execute(
        update(User)
        .where(User.id == user_id)
        .values(is_active=True)
    )
    await db.commit()
    
    return SuccessResponse(message=f"User {user.email} has been activated")


@router.post(
    "/users/{user_id}/deactivate",
    response_model=SuccessResponse,
    summary="Deactivate User",
    description="Admin-only endpoint to deactivate a user account",
    responses={
        200: {"description": "User deactivated successfully"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden - Admin access required"},
        404: {"description": "User not found"}
    }
)
async def deactivate_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
) -> SuccessResponse:
    """Deactivate a user account - Admin only."""
    from app.services.user_service import UserService
    from sqlalchemy import update
    
    user_service = UserService()
    user = await user_service.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.is_active:
        return SuccessResponse(message="User is already inactive")
    
    # Prevent deactivating self
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )
    
    # Deactivate user
    await db.execute(
        update(User)
        .where(User.id == user_id)
        .values(is_active=False)
    )
    await db.commit()
    
    # Revoke all user tokens
    from app.core.auth import revoke_token
    await revoke_token(db, "", revoke_all=True, user_id=user_id)
    
    return SuccessResponse(message=f"User {user.email} has been deactivated")


@router.post(
    "/cleanup-tokens",
    response_model=SuccessResponse,
    summary="Cleanup Expired Tokens",
    description="Admin-only endpoint to manually cleanup expired tokens",
    responses={
        200: {"description": "Tokens cleaned up successfully"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden - Admin access required"}
    }
)
async def cleanup_expired_tokens_admin(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
) -> SuccessResponse:
    """Manually cleanup expired tokens - Admin only."""
    from app.core.auth import cleanup_expired_tokens
    
    cleaned_count = await cleanup_expired_tokens(db)
    
    return SuccessResponse(
        message=f"Cleaned up {cleaned_count} expired tokens"
    )


@router.get(
    "/my-scopes",
    response_model=SuccessResponse,
    summary="Get My Scopes",
    description="Get current user's scopes/permissions",
    responses={
        200: {"description": "Scopes retrieved successfully"},
        401: {"description": "Unauthorized"}
    }
)
async def get_my_scopes(
    current_user: User = Depends(require_user),
    db: AsyncSession = Depends(get_db)
) -> SuccessResponse:
    """Get current user's scopes - User access required."""
    from app.core.auth import get_user_scopes
    
    scopes = await get_user_scopes(current_user, db)
    
    return SuccessResponse(
        message="Scopes retrieved successfully",
        data={
            "user_id": current_user.id,
            "email": current_user.email,
            "scopes": scopes,
            "is_superuser": current_user.is_superuser
        }
    )
