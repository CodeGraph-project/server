from fastapi import APIRouter, Response, Cookie
from app.core.config import settings


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/me")
async def get_me(response: Response):
    pass