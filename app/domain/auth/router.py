from fastapi import APIRouter, Request



auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/github/login")
async def login(request: Request) -> dict:
    pass


@auth_router.get("/github/callback")
async def callback(request: Request) -> dict:
    pass


@auth_router.post("/refresh")
async def refresh(request: Request) -> dict:
    pass


@auth_router.post("/logout")
async def logout(request: Request) -> dict:
    pass