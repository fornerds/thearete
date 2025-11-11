"""Database model for TREATMENT table."""

from datetime import datetime
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, BigInteger, SmallInteger
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List, Optional

from app.db.base import Base


class Treatment(Base):
    """Treatment model."""
    
    __tablename__ = "treatment"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, nullable=False)
    customer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("customer.id"), nullable=False)
    type: Mapped[Optional[str]] = mapped_column(String(255), comment="시술 종류 (튼살-경, 튼살-중, 백반증, 흉터 등)")
    area: Mapped[Optional[str]] = mapped_column(String(255), comment="시술 부위 (얼굴, 목, 팔, 다리, 입술 등)")
    is_completed: Mapped[Optional[bool]] = mapped_column(Boolean, comment="시술 완료 여부")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: Mapped[Optional[bool]] = mapped_column(Boolean)

    # Relationships
    customer: Mapped["Customer"] = relationship(
        "Customer",
        back_populates="treatment",
        lazy="selectin",
    )
    treatment_session: Mapped[List["TreatmentSession"]] = relationship(
        "TreatmentSession",
        back_populates="treatment",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    photo: Mapped[List["Photo"]] = relationship("Photo", back_populates="treatment", cascade="all, delete-orphan")
    def __repr__(self) -> str:
        return f"<Treatment(id={self.id}, customer_id='{self.customer_id}', type='{self.type}')>"
