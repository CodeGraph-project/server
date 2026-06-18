import enum
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, BigInteger, DateTime, Enum as SAEnum


class UserRole(enum.StrEnum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    GUEST = "GUEST"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True, sa_type=BigInteger)

    github_id: int = Field(sa_type=BigInteger, unique=True, index=True)

    username: str = Field(max_length=40, unique=True, index=True)

    avatar_url: Optional[str] = Field(default=None, max_length=300)

    role: UserRole = Field(
        default=UserRole.MEMBER,
        sa_type=SAEnum(UserRole, native_enum=False, length=20),
        nullable=False,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )