import enum
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, BigInteger, DateTime, Text, Enum as SAEnum


class PatternCategory(enum.StrEnum):
    AUTH = "AUTH"
    ERROR_HANDLING = "ERROR_HANDLING"
    SEARCH = "SEARCH"
    DATABASE = "DATABASE"
    API = "API"
    OTHER = "OTHER"
    # 일단 여기까지만


class Pattern(SQLModel, table=True):
    __tablename__ = "patterns"

    id: Optional[int] = Field(default=None, primary_key=True, sa_type=BigInteger)

    category: PatternCategory = Field(
        sa_type=SAEnum(PatternCategory, native_enum=False, length=20),
        nullable=False,
        index=True,
    )
    name: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, sa_type=Text)
    project_count: int = Field(default=0)   # 이 패턴이 발견된 프로젝트 수

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )


class PatternExample(SQLModel, table=True):
    __tablename__ = "pattern_examples"

    id: Optional[int] = Field(default=None, primary_key=True, sa_type=BigInteger)
    pattern_id: int = Field(foreign_key="patterns.id", sa_type=BigInteger, index=True)
    repo_id: int = Field(foreign_key="repos.id", sa_type=BigInteger, index=True)

    file_path: str = Field(max_length=500)
    code_text: str = Field(sa_type=Text)
    note: Optional[str] = Field(default=None, sa_type=Text)