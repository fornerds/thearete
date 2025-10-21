"""User token model for refresh token blacklist."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserToken(Base):
    """User token model for managing refresh tokens and sessions."""
    
    __tablename__ = "user_tokens"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    token_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "refresh", "access"
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    device_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # User agent, IP 등
    session_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="tokens")
    
    def __repr__(self) -> str:
        return f"<UserToken(id={self.id}, user_id={self.user_id}, token_type='{self.token_type}', is_revoked={self.is_revoked})>"
    
    @property
    def is_expired(self) -> bool:
        """Check if token is expired."""
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        """Check if token is valid (not revoked and not expired)."""
        return not self.is_revoked and not self.is_expired
