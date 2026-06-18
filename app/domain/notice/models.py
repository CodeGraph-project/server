from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, BigInteger, DateTime, Text


class Notice(SQLModel, table=True):
    __tablename__ = "notices"

    id: Optional[int] = Field(default=None, primary_key=True, sa_type=BigInteger)
    author_id: int = Field(foreign_key="users.id", sa_type=BigInteger, index=True)

    title: str = Field(max_length=200)
    body: str = Field(sa_type=Text)
    pinned: bool = Field(default=False, index=True)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )