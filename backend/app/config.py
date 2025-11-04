"""FastAPI application configuration using Pydantic Settings."""

from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = Field(..., description="Database connection URL")

    # Security
    secret_key: str = Field(..., description="Secret key for JWT tokens")
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        default=30, description="Access token expiration in minutes"
    )
    refresh_token_expire_minutes: int = Field(
        default=10080, description="Refresh token expiration in minutes"
    )

    # App
    app_name: str = Field(default="mobile-backend", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    host: str = Field(default="0.0.0.0", description="Host to bind to")
    port: int = Field(default=8000, description="Port to bind to")

    # CORS
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="Allowed CORS origins",
    )
    allowed_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="Allowed CORS methods",
    )
    allowed_headers: List[str] = Field(
        default=["*"], description="Allowed CORS headers"
    )

    # AI Configuration
    ai_provider: str = Field(
        default="mock", 
        description="AI provider (openai, anthropic, generic, mock)"
    )
    ai_base_url: str = Field(
        default="https://api.openai.com/v1",
        description="AI API base URL"
    )
    ai_api_key: str = Field(
        default="",
        description="AI API key"
    )
    ai_timeout_sec: int = Field(
        default=30,
        description="AI request timeout in seconds"
    )
    ai_max_retries: int = Field(
        default=3,
        description="Maximum number of retries for AI requests"
    )
    ai_circuit_breaker_threshold: int = Field(
        default=5,
        description="Circuit breaker failure threshold"
    )
    ai_circuit_breaker_timeout: int = Field(
        default=60,
        description="Circuit breaker recovery timeout in seconds"
    )

    # Database Seeding
    seed_on_start: bool = Field(
        default=False,
        description="Automatically seed database on application startup"
    )


# Global settings instance
settings = Settings()
