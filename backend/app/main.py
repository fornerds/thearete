"""FastAPI application with routers and middleware."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import (
    routes_auth,
    routes_health,
    routes_ai,
    routes_shop,
    routes_customer,
    routes_treatment,
    routes_treatment_sessions,
    routes_skin_measurements,
    routes_color_recipes,
    routes_treatment_photos,
    routes_uploads,
)
from app.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.uploads import get_upload_root
from app.db.session import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    create_tables()
    
    # Auto-seed database if enabled
    if settings.seed_on_start:
        try:
            from app.scripts.seed import seed_database
            await seed_database()
            print("✅ Database seeded successfully on startup")
        except Exception as e:
            print(f"⚠️  Failed to seed database on startup: {e}")
    
    yield
    # Shutdown
    pass


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI mobile backend with JWT authentication and comprehensive security features",
    debug=settings.debug,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "User authentication and token management operations",
        },
        {
            "name": "Health",
            "description": "Health check and monitoring endpoints",
        },
        {
            "name": "AI",
            "description": "AI service operations for text completion and embeddings",
        },
    ],
)

# Upload directory initialization (files are served via Nginx X-Accel-Redirect)
# Static file serving is handled by Nginx, not FastAPI
upload_root = get_upload_root(settings.upload_root)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

# Register exception handlers
register_exception_handlers(app)

# Include routers
app.include_router(routes_health.router, prefix="/v1")
app.include_router(routes_auth.router, prefix="/v1")
app.include_router(routes_ai.router, prefix="/v1")
app.include_router(routes_shop.router, prefix="/api")
app.include_router(routes_customer.router, prefix="/api")
app.include_router(routes_treatment.router)
app.include_router(routes_treatment_sessions.router)
app.include_router(routes_skin_measurements.router)
app.include_router(routes_color_recipes.router)
app.include_router(routes_treatment_photos.router)
app.include_router(routes_uploads.router)
app.include_router(routes_uploads.download_router)


@app.get("/")
async def root() -> JSONResponse:
    """Root endpoint."""
    return JSONResponse(
        content={
            "message": f"Welcome to {settings.app_name}",
            "version": settings.app_version,
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/v1/health",
        }
    )
