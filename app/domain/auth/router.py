from fastapi import APIRouter, Response, Cookie
from fastapi.responses import RedirectResponse
from app.core.config import settings
from app.domain.auth.dependencies import AuthServiceDep
from app.domain.auth.schemas import AuthorizeUrlResponse, TokenResponse


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/github/login", response_model=AuthorizeUrlResponse)
async def login(service: AuthServiceDep):
    url = await service.create_authorize_urls()
    return AuthorizeUrlResponse(authorize_url=url)


@auth_router.get("/github/callback")
async def callback(code: str, state: str, service: AuthServiceDep):
    access, refresh = await service.handle_callback(code, state)
    # resp = RedirectResponse(url=f"{settings.FRONTEND_URL}/auth/callback#access_token={access}")
    # _set_refresh_cookie(resp, refresh)
    # return resp
    return {"access_token": access, "refresh_token": refresh} # 스웨거 테스트용


@auth_router.post("/refresh")#, response_model=TokenResponse)
async def refresh(
        service: AuthServiceDep,
        # response: Response,
        # refresh_token: str | None = Cookie(default=None)
        refresh_token: str # 스웨거 테스트용
):
    access, new_refresh = await service.refresh(refresh_token)
    # _set_refresh_cookie(response, new_refresh)
    # return TokenResponse(access_token=access)
    return {"access_token": access, "refresh_token": new_refresh} # 스웨거 테스트용


@auth_router.post("/logout")
async def logout(
        service: AuthServiceDep,
        # response: Response,
        # refresh_token: str | None = Cookie(default=None)
        refresh_token: str # 스웨거 테스트용
):
    await service.logout(refresh_token)
    # response.delete_cookie(key="refresh_token", path="/auth")
    return {"message": 'logout'}


def _set_refresh_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key='refresh_token',
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        path="/auth",
    )