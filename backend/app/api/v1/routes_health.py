"""Health check routes."""

import asyncio
import time
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.config import settings
from app.db.session import get_db
from app.schemas.common import HealthResponse, ServiceHealth, HealthStatus
from app.ai.client import AIClient

router = APIRouter(prefix="/v1/health", tags=["Health"])

# Track application start time
app_start_time = time.time()


async def check_database(db: AsyncSession) -> ServiceHealth:
    """Check database connectivity."""
    start_time = time.time()
    
    try:
        # Simple query to check database connectivity
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return ServiceHealth(
            name="database",
            status=HealthStatus.HEALTHY,
            response_time_ms=round(response_time, 2)
        )
    except Exception as e:
        response_time = (time.time() - start_time) * 1000
        
        return ServiceHealth(
            name="database",
            status=HealthStatus.UNHEALTHY,
            response_time_ms=round(response_time, 2),
            error=str(e)
        )


async def check_ai_service() -> ServiceHealth:
    """Check AI service connectivity."""
    start_time = time.time()
    
    try:
        ai_client = AIClient()
        
        # Simple ping to AI service
        await ai_client.ping()
        
        response_time = (time.time() - start_time) * 1000
        
        return ServiceHealth(
            name="ai_service",
            status=HealthStatus.HEALTHY,
            response_time_ms=round(response_time, 2)
        )
    except Exception as e:
        response_time = (time.time() - start_time) * 1000
        
        return ServiceHealth(
            name="ai_service",
            status=HealthStatus.UNHEALTHY,
            response_time_ms=round(response_time, 2),
            error=str(e)
        )


async def check_token_cleanup(db: AsyncSession) -> ServiceHealth:
    """Check token cleanup service."""
    start_time = time.time()
    
    try:
        from app.core.auth import cleanup_expired_tokens
        
        # Clean up expired tokens
        cleaned_count = await cleanup_expired_tokens(db)
        
        response_time = (time.time() - start_time) * 1000
        
        return ServiceHealth(
            name="token_cleanup",
            status=HealthStatus.HEALTHY,
            response_time_ms=round(response_time, 2)
        )
    except Exception as e:
        response_time = (time.time() - start_time) * 1000
        
        return ServiceHealth(
            name="token_cleanup",
            status=HealthStatus.UNHEALTHY,
            response_time_ms=round(response_time, 2),
            error=str(e)
        )


@router.get(
    "/",
    response_model=HealthResponse,
    summary="Health Check",
    description="Comprehensive health check for all services",
    responses={
        200: {"description": "Health check completed"},
        503: {"description": "Service unhealthy"}
    }
)
async def health_check(db: AsyncSession = Depends(get_db)) -> HealthResponse:
    """Comprehensive health check endpoint."""
    # Run all health checks concurrently
    health_checks = [
        check_database(db),
        check_ai_service(),
        check_token_cleanup(db)
    ]
    
    services = await asyncio.gather(*health_checks, return_exceptions=True)
    
    # Handle any exceptions
    processed_services = []
    for service in services:
        if isinstance(service, Exception):
            processed_services.append(ServiceHealth(
                name="unknown",
                status=HealthStatus.UNHEALTHY,
                error=str(service)
            ))
        else:
            processed_services.append(service)
    
    # Determine overall status
    unhealthy_services = [s for s in processed_services if s.status == HealthStatus.UNHEALTHY]
    
    if unhealthy_services:
        overall_status = HealthStatus.UNHEALTHY
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        overall_status = HealthStatus.HEALTHY
        status_code = status.HTTP_200_OK
    
    response = HealthResponse(
        success=True,
        status=overall_status,
        services=processed_services,
        version=getattr(settings, 'app_version', '1.0.0')
    )
    
    if overall_status == HealthStatus.UNHEALTHY:
        raise HTTPException(status_code=status_code, detail=response.dict())
    
    return response


@router.get(
    "/ready",
    summary="Readiness Check",
    description="Check if the service is ready to accept traffic",
    responses={
        200: {"description": "Service is ready"},
        503: {"description": "Service is not ready"}
    }
)
async def readiness_check(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Readiness check endpoint."""
    try:
        # Check critical services for readiness
        db_health = await check_database(db)
        
        if db_health.status != HealthStatus.HEALTHY:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not ready"
            )
        
        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {
                "database": "ok"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service not ready: {str(e)}"
        )


@router.get(
    "/live",
    summary="Liveness Check",
    description="Check if the service is alive",
    responses={
        200: {"description": "Service is alive"}
    }
)
async def liveness_check() -> Dict[str, Any]:
    """Liveness check endpoint."""
    uptime_seconds = time.time() - app_start_time
    
    return {
        "status": "alive",
        "uptime_seconds": round(uptime_seconds, 2),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get(
    "/ping",
    summary="Simple Ping",
    description="Simple ping endpoint for basic connectivity check",
    responses={
        200: {"description": "Pong"}
    }
)
async def ping() -> Dict[str, str]:
    """Simple ping endpoint."""
    return {"message": "pong"}
