from typing import Annotated
from fastapi import Depends
from app.domain.user.models import User, UserRole
from app.domain.user.dependencies import UserRepositoryDep, CurrentUser
from app.domain.admin.service import AdminService


def require_role(*allowed: UserRole):
    async def checker(user: CurrentUser) -> User:
        if user.role not in allowed:
            pass
        return user
    return checker

CurrentAdmin = Annotated[User, Depends(require_role(UserRole.ADMIN))]


def get_admin_service(user_repo: UserRepositoryDep) -> AdminService:
    return AdminService(user_repo)

AdminServiceDep = Annotated[AdminService, Depends(get_admin_service)]