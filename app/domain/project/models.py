import enum
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field,  BigInteger, DateTime, Text, Enum as SAEnum


class ProjectStatus(enum.StrEnum):
    PENDING = "PENDING"      # 등록 신청
    ACTIVE = "ACTIVE"        # 승인 + 인덱싱 완료
    REJECTED = "REJECTED"    # 반려됨
    ARCHIVED = "ARCHIVED"    # 보관 (비활성화한거)


class ProjectCategory(enum.StrEnum):
    CLASS = "CLASS"          # 수업
    TEAM = "TEAM"            # 팀 프로젝트
    PERSONAL = "PERSONAL"    # 개인
    CONTEST = "CONTEST"      # 대회
    # 기타 항목 추가할거임


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: Optional[int] = Field(default=None, primary_key=True, sa_type=BigInteger)

    owner_id: int = Field(foreign_key="users.id", sa_type=BigInteger, index=True)

    name: str = Field(max_length=100)
    slug: str = Field(max_length=120, unique=True, index=True)

    description: Optional[str] = Field(default=None, sa_type=Text)
    overview: Optional[str] = Field(default=None, sa_type=Text)

    logo_url: Optional[str] = Field(default=None, max_length=1000)
    year: int

    category: ProjectCategory = Field(
        sa_type=SAEnum(ProjectCategory, native_enum=False, length=20),
        nullable=False,
    )
    status: ProjectStatus = Field(
        default=ProjectStatus.PENDING,
        sa_type=SAEnum(ProjectStatus, native_enum=False, length=20),
        nullable=False,
    )
    reject_reason: Optional[str] = Field(default=None, sa_type=Text)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )


class ProjectMember(SQLModel, table=True):
    __tablename__ = "project_members"

    project_id: int = Field(foreign_key="projects.id", sa_type=BigInteger, primary_key=True)
    user_id: int = Field(foreign_key="users.id", sa_type=BigInteger, primary_key=True)

    joined_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )