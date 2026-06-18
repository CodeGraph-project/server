import enum
from datetime import datetime, timezone
from typing import Any, Optional
from sqlalchemy.dialects.postgresql import TSVECTOR
from pgvector.sqlalchemy import Vector
from sqlmodel import SQLModel, Field, BigInteger, DateTime, Text, Enum as SAEnum

EMBED_DIM = 1024


class ChunkType(enum.StrEnum):
    FUNCTION = "FUNCTION"
    CLASS = "CLASS"
    METHOD = "METHOD"
    CONFIG = "CONFIG"
    IMPORT = "IMPORT"


class CodeChunk(SQLModel, table=True):
    __tablename__ = "code_chunks"

    id: Optional[int] = Field(default=None, primary_key=True, sa_type=BigInteger)

    repo_id: int = Field(foreign_key="repos.id", sa_type=BigInteger, index=True)
    # 프젝 단위 필터링 하기 위한 컬럼
    project_id: int = Field(foreign_key="projects.id", sa_type=BigInteger, index=True)

    file_path: str = Field(max_length=500)
    language: Optional[str] = Field(default=None, max_length=50)
    chunk_type: ChunkType = Field(
        sa_type=SAEnum(ChunkType, native_enum=False, length=20),
        nullable=False,
    )

    name: Optional[str] = Field(default=None, max_length=300)   # 함수/클래스 이름
    signature: Optional[str] = Field(default=None, sa_type=Text)
    code_text: str = Field(sa_type=Text)

    # 코드 원문 임베딩: 코드 용어 검색용
    code_embedding: Optional[Any] = Field(default=None, sa_type=Vector(EMBED_DIM))
    # LLM 생성 설명 임베딩: 의미/의도 검색용
    desc_embedding: Optional[Any] = Field(default=None, sa_type=Vector(EMBED_DIM))
    # 함수/클래스/변수명 풀텍스트 검색용
    fts_tsv: Optional[Any] = Field(default=None, sa_type=TSVECTOR)

    start_line: int
    end_line: int

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )