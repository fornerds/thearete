"""Database model for TREATMENT_SESSION table."""

from datetime import datetime
from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, BigInteger, SmallInteger
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List, Optional

from app.db.base import Base


class TreatmentSession(Base):
    """TreatmentSession model."""
    
    __tablename__ = "treatment_session"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, nullable=False)
    treatment_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("treatment.id"), nullable=False)
    treatment_date: Mapped[Optional[datetime]] = mapped_column(Date, comment="시술 날짜")
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, comment="소요시간(분)")
    melanin: Mapped[Optional[int]] = mapped_column(Integer, comment="멜라닌 투입량 (0~9)")
    white: Mapped[Optional[int]] = mapped_column(Integer, comment="화이트 투입량 (0~9)")
    red: Mapped[Optional[int]] = mapped_column(Integer, comment="레드 투입량 (0~9)")
    yellow: Mapped[Optional[int]] = mapped_column(Integer, comment="옐로우 투입량 (0~9)")
    is_completed: Mapped[Optional[bool]] = mapped_column(Boolean, comment="시술 완료 여부")
    is_result_entered: Mapped[Optional[int]] = mapped_column(SmallInteger, comment="시술 결과 입력 저장 여부")
    note: Mapped[Optional[str]] = mapped_column(Text, comment="특이사항")
    first_recorded_at: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="최초 작성시간")
    last_modified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="최종 수정시간")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: Mapped[Optional[bool]] = mapped_column(Boolean)

    # Relationships
    treatment: Mapped["Treatment"] = relationship("Treatment", back_populates="treatment_session")
    skin_color_measurement: Mapped[List["SkinColorMeasurement"]] = relationship("SkinColorMeasurement", back_populates="treatment_session", cascade="all, delete-orphan")
    photo: Mapped[List["Photo"]] = relationship("Photo", back_populates="treatment_session", cascade="all, delete-orphan")
    def __repr__(self) -> str:
        return f"<TreatmentSession(id={self.id}, treatment_id='{self.treatment_id}', treatment_date='{self.treatment_date}')>"
