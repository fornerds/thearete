"""Database model linking treatment sessions to uploaded images."""

from datetime import datetime

from typing import Optional

from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TreatmentSessionImage(Base):
    """Associate uploaded images with treatment sessions."""

    __tablename__ = "treatment_session_image"
    __table_args__ = ()

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    treatment_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("treatment.id"), nullable=False)
    session_id: Mapped[int] = mapped_column("session_id", BigInteger, ForeignKey("treatment_session.id"), nullable=False)
    uploaded_image_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("uploaded_image.id"), nullable=False)
    photo_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    uploaded_image = relationship("UploadedImage", back_populates="treatment_session_images")
    session = relationship("TreatmentSession", back_populates="images")
    treatment = relationship("Treatment", back_populates="images")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<TreatmentSessionImage(session_id={self.session_id}, image_id={self.uploaded_image_id})>"

