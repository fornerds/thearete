"""Database model for PHOTO table."""

from datetime import datetime
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, BigInteger, SmallInteger
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List, Optional

from app.db.base import Base


class Photo(Base):
    """Photo model."""
    
    __tablename__ = "photo"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, nullable=False)
    treatment_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("treatment.id"), nullable=False)
    session_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("treatment_session.id"), nullable=True, comment="nullable (회차에 속하지 않을 수도 있음)")
    photo_type: Mapped[Optional[str]] = mapped_column(String, comment="BEFORE | AFTER")
    file_url: Mapped[Optional[str]] = mapped_column(String(255), comment="저장 경로")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: Mapped[Optional[bool]] = mapped_column(Boolean)

    # Relationships
    treatment: Mapped["Treatment"] = relationship("Treatment", back_populates="photo")
    treatment_session: Mapped["TreatmentSession"] = relationship("TreatmentSession", back_populates="photo")
    def __repr__(self) -> str:
        return f"<Photo(id={self.id}, treatment_id='{self.treatment_id}', session_id='{self.session_id}')>"
