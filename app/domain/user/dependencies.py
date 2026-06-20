from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.database import AsyncSessionDep
from app.core.security import security_handler
from app.domain.user.models import User
from app.domain.user.repository import UserRepository
from app.domain.user.service import UserService
from app.domain.project.dependencies import GetProjectRepository
from app.domain.scrap.dependencies import GetScrapRepository


def get_user_repository(session: AsyncSessionDep) -> UserRepository:
    return UserRepository(session)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_service(
    user_repo: UserRepositoryDep,
    project_repo: GetProjectRepository,
    scrap_repo: GetScrapRepository,
) -> UserService:
    return UserService(user_repo, project_repo, scrap_repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]


bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    user_repo: UserRepositoryDep,
) -> User:
    payload = security_handler.decode_token(credentials.credentials)

    if not payload or payload.get("type") != "access":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid access token")

    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid token payload")

    user = await user_repo.get_user_by_id(int(sub))
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "user not found")

    return user

CurrentUser = Annotated[User, Depends(get_current_user)]