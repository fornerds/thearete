"""Database model for SHOP table."""

from datetime import datetime
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Integer, BigInteger, SmallInteger
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List, Optional

from app.db.base import Base


class Shop(Base):
    """Shop model."""
    
    __tablename__ = "shop"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255), comment="상호명")
    address: Mapped[Optional[str]] = mapped_column(String(255), comment="주소")
    owner_name: Mapped[Optional[str]] = mapped_column(String(255), comment="대표자명")
    phone: Mapped[Optional[str]] = mapped_column(String(255), comment="전화번호")
    email: Mapped[Optional[str]] = mapped_column(String(255), comment="이메일 (로그인 ID)")
    password: Mapped[Optional[str]] = mapped_column(String(255), comment="비밀번호 (암호화 저장)")
    refresh_token: Mapped[Optional[str]] = mapped_column(String(255), comment="현재 로그인 중인 Refresh Token 저장")
    refresh_token_expiry: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="Refresh Token 만료 일시")
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="마지막 로그인 시간 (선택)")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: Mapped[Optional[bool]] = mapped_column(Boolean)

    # Relationships
    customer: Mapped[List["Customer"]] = relationship("Customer", back_populates="shop", cascade="all, delete-orphan")
    def __repr__(self) -> str:
        return f"<Shop(id={self.id}, name='{self.name}', address='{self.address}')>"
