from fastapi import Depends
from typing import Annotated
from collections.abc import AsyncGenerator
import redis.asyncio as aioredis
from app.core.config import settings

redis_client = aioredis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True,
)

async def get_redis_client() -> AsyncGenerator[aioredis.Redis, None]:
        yield redis_client

async def close_redis():
    await redis_client.aclose()

RedisDep = Annotated[aioredis.Redis, Depends(get_redis_client)]