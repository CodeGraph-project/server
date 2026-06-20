from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.redis import close_redis
from app.domain.auth.router import auth_router
from app.domain.user.router import user_router
from app.domain.admin.router import admin_router

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield
    await close_redis()

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)