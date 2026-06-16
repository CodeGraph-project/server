import enum
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Enum, Column, func, DateTime


class UserRole(enum.StrEnum):
    GUEST = "Guest"
    MEMBER = "Member"
    ADMIN = "Admin"


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    github_id: int = Field(unique=True, nullable=False)
    username: str = Field(unique=True, nullable=False)
    avatar_url: str
    role: UserRole = Field(sa_column=Column(Enum(UserRole), nullable=False))
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )








