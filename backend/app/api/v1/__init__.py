"""API v1 package."""

from fastapi import APIRouter

# Create main API router
router = APIRouter()

# Import and include sub-routers
from app.api.v1.routes_health import router as health_router  # noqa: E402
from app.api.v1.routes_auth import router as auth_router  # noqa: E402
from app.api.v1.routes_items import router as items_router  # noqa: E402

# Include routers
router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(items_router, prefix="/items", tags=["items"])
