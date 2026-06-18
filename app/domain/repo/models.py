import enum
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, BigInteger, DateTime, Enum as SAEnum


class RepoStatus(enum.StrEnum):
    PENDING = "PENDING"      # 추가 신청, 승인 대기
    INDEXING = "INDEXING"    # 인덱싱 진행 중
    ACTIVE = "ACTIVE"        # 인덱싱 완료
    FAILED = "FAILED"        # 인덱싱 실패
    ARCHIVED = "ARCHIVED"    # 보관


class RepoRole(enum.StrEnum):
    BACKEND = "BACKEND"
    FRONTEND = "FRONTEND"
    AI_ML = "AI_ML"
    OTHER = "OTHER"


class Repo(SQLModel, table=True):
    __tablename__ = "repos"

    id: Optional[int] = Field(default=None, primary_key=True, sa_type=BigInteger)

    project_id: int = Field(foreign_key="projects.id", sa_type=BigInteger, index=True)

    name: str = Field(max_length=200)
    github_url: str = Field(max_length=500)
    language: Optional[str] = Field(default=None, max_length=50)

    role: RepoRole = Field(
        sa_type=SAEnum(RepoRole, native_enum=False, length=20),
        nullable=False,
    )
    status: RepoStatus = Field(
        default=RepoStatus.PENDING,
        sa_type=SAEnum(RepoStatus, native_enum=False, length=20),
        nullable=False,
    )

    last_commit_hash: Optional[str] = Field(default=None, max_length=40)  # 증분 인덱싱 비교용임
    last_indexed_at: Optional[datetime] = Field(default=None, sa_type=DateTime(timezone=True))
    chunk_count: int = Field(default=0)