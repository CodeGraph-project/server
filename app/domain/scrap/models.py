import enum
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, BigInteger, DateTime, Text, Enum as SAEnum


class ScrapSource(enum.StrEnum):
    VIEWER = "VIEWER"    # 코드 뷰어 스크랩
    CHAT = "CHAT"        # AI 채팅 스크랩


class ScrapFolder(SQLModel, table=True):
    __tablename__ = "scrap_folders"

    id: Optional[int] = Field(default=None, primary_key=True, sa_type=BigInteger)
    user_id: int = Field(foreign_key="users.id", sa_type=BigInteger, index=True)
    name: str = Field(max_length=100)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )


class Scrap(SQLModel, table=True):
    __tablename__ = "scraps"

    id: Optional[int] = Field(default=None, primary_key=True, sa_type=BigInteger)
    user_id: int = Field(foreign_key="users.id", sa_type=BigInteger, index=True)
    # folder_id 가 NULL 이면 '미분류'
    folder_id: Optional[int] = Field(
        default=None, foreign_key="scrap_folders.id", sa_type=BigInteger, index=True
    )

    project_name: str = Field(max_length=100)
    file_path: str = Field(max_length=500)
    code_text: str = Field(sa_type=Text)
    memo: Optional[str] = Field(default=None, sa_type=Text)

    source: ScrapSource = Field(
        sa_type=SAEnum(ScrapSource, native_enum=False, length=10),
        nullable=False,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )