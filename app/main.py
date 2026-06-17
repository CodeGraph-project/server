from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.redis import close_redis
from app.domain.auth.router import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield
    await close_redis()

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)