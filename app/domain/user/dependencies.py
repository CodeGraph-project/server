from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.database import AsyncSessionDep
from app.core.security import security_handler
from app.domain.user.models import User, UserRole
from app.domain.user.repository import UserRepository
from app.domain.user.service import UserService


def get_user_repository(session: AsyncSessionDep) -> UserRepository:
    return UserRepository(session)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_service(user_repo: UserRepositoryDep) -> UserService:
    return UserService(user_repo)

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


def require_role(*allowed: UserRole):
    async def checker(user: CurrentUser) -> User:
        if user.role not in allowed:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "forbidden")
        return user
    return checker

CurrentAdmin = Annotated[User, Depends(require_role(UserRole.ADMIN))]