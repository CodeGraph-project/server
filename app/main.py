from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.redis import close_redis

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield
    await close_redis()

app = FastAPI(lifespan=lifespan)
