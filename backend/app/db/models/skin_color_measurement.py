"""Database model for SKIN_COLOR_MEASUREMENT table."""

from datetime import datetime
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, BigInteger, SmallInteger
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List, Optional

from app.db.base import Base


class SkinColorMeasurement(Base):
    """SkinColorMeasurement model."""
    
    __tablename__ = "skin_color_measurement"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, nullable=False)
    session_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("treatment_session.id"), nullable=False)
    region_type: Mapped[Optional[str]] = mapped_column(String, comment="NORMAL | LESION")
    l_value: Mapped[Optional[float]] = mapped_column(Float, comment="L 값")
    a_value: Mapped[Optional[float]] = mapped_column(Float, comment="a 값")
    b_value: Mapped[Optional[float]] = mapped_column(Float, comment="b 값")
    measurement_point: Mapped[Optional[str]] = mapped_column(String(255), comment="측정 위치(선택적)")
    measured_at: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="측정 시각")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: Mapped[Optional[bool]] = mapped_column(Boolean)

    # Relationships
    treatment_session: Mapped["TreatmentSession"] = relationship("TreatmentSession", back_populates="skin_color_measurement")
    def __repr__(self) -> str:
        return f"<SkinColorMeasurement(id={self.id}, session_id='{self.session_id}', region_type='{self.region_type}')>"
