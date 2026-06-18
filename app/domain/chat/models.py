import enum
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, BigInteger, DateTime, Text, Enum as SAEnum


class MessageRole(enum.StrEnum):
    USER = "USER"
    AI = "AI"


class ChatSession(SQLModel, table=True):
    __tablename__ = "chat_sessions"

    id: Optional[int] = Field(default=None, primary_key=True, sa_type=BigInteger)
    user_id: int = Field(foreign_key="users.id", sa_type=BigInteger, index=True)
    title: str = Field(max_length=200)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"

    id: Optional[int] = Field(default=None, primary_key=True, sa_type=BigInteger)
    session_id: int = Field(foreign_key="chat_sessions.id", sa_type=BigInteger, index=True)

    role: MessageRole = Field(
        sa_type=SAEnum(MessageRole, native_enum=False, length=10),
        nullable=False,
    )
    content: str = Field(sa_type=Text)
    # 답변이 참조한 코드 청크들 [{repo, file_path, start_line, end_line}, ...]
    code_refs: Optional[list] = Field(default=None, sa_type=JSONB)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )