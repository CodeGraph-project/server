import enum
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, BigInteger, DateTime, Text, Enum as SAEnum


class InquiryType(enum.StrEnum):
    IMPROVEMENT = "IMPROVEMENT"   # 개선 요청
    BUG = "BUG"                   # 버그 제보
    OTHER = "OTHER"               # 기타


class Inquiry(SQLModel, table=True):
    __tablename__ = "inquiries"

    id: Optional[int] = Field(default=None, primary_key=True, sa_type=BigInteger)
    user_id: int = Field(foreign_key="users.id", sa_type=BigInteger, index=True)

    type: InquiryType = Field(
        sa_type=SAEnum(InquiryType, native_enum=False, length=20),
        nullable=False,
    )
    content: str = Field(sa_type=Text)
    is_read: bool = Field(default=False, index=True)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )