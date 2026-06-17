from typing import Annotated
from fastapi import Depends
from app.core.database import AsyncSessionDep
from app.core.redis import RedisDep
from app.domain.user.repository import UserRepository
from app.infrastructure.github.oauth import GitHubOAuth
from app.domain.auth.service import AuthService


def get_user_repository(session: AsyncSessionDep) -> UserRepository:
    return UserRepository(session)


def get_github_oauth() -> GitHubOAuth:
    return GitHubOAuth()


def get_auth_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    github: Annotated[GitHubOAuth, Depends(get_github_oauth)],
    redis: RedisDep,
) -> AuthService:
    return AuthService(user_repo=user_repo, github=github, redis=redis)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]