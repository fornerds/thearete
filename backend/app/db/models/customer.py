"""Database model for CUSTOMER table."""

from datetime import datetime
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, BigInteger, SmallInteger
from sqlalchemy import String, Text
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List, Optional

from app.db.base import Base


class Customer(Base):
    """Customer model."""
    
    __tablename__ = "customer"
    __table_args__ = (
        UniqueConstraint(
            "shop_id",
            "phone",
            "name",
            name="uq_customer_shop_phone_name",
        ),
    )
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, nullable=False)
    shop_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("shop.id"), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255), comment="고객명")
    age: Mapped[Optional[int]] = mapped_column(Integer, comment="나이")
    gender: Mapped[Optional[str]] = mapped_column(Enum("M", "F", name="gender_enum", create_type=False), comment="성별 (M/F)")
    phone: Mapped[Optional[str]] = mapped_column(String(255), comment="연락처")
    skin_type: Mapped[Optional[str]] = mapped_column(String(255), comment="피부타입")
    note: Mapped[Optional[str]] = mapped_column(Text, comment="특이사항")
    marked: Mapped[Optional[int]] = mapped_column(SmallInteger, comment="상단 고정 여부")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: Mapped[Optional[bool]] = mapped_column(Boolean)

    # Relationships
    shop: Mapped["Shop"] = relationship("Shop", back_populates="customer")
    treatment: Mapped[List["Treatment"]] = relationship(
        "Treatment",
        back_populates="customer",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    def __repr__(self) -> str:
        return f"<Customer(id={self.id}, shop_id='{self.shop_id}', name='{self.name}')>"
