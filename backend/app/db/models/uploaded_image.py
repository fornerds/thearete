"""Database model for uploaded images."""

from datetime import datetime

from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UploadedImage(Base):
    """Store metadata for images uploaded via the dedicated upload API."""

    __tablename__ = "uploaded_image"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    original_filename: Mapped[Optional[str]] = mapped_column(String(255))
    storage_path: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    public_url: Mapped[str] = mapped_column(String(255), nullable=False)
    thumbnail_storage_path: Mapped[Optional[str]] = mapped_column(String(255))
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(255))
    content_type: Mapped[Optional[str]] = mapped_column(String(128))
    file_size: Mapped[Optional[int]] = mapped_column(Integer)
    thumbnail_size: Mapped[Optional[int]] = mapped_column(Integer)
    storage_backend: Mapped[str] = mapped_column(String(50), default="local")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    treatment_session_images = relationship(
        "TreatmentSessionImage",
        back_populates="uploaded_image",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<UploadedImage(id={self.id}, storage_path='{self.storage_path}')>"

