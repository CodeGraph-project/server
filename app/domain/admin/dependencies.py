from typing import Annotated
from fastapi import Depends, HTTPException,status
from app.domain.user.models import User, UserRole
from app.domain.user.dependencies import UserRepositoryDep, CurrentUser
from app.domain.admin.service import AdminService


def require_role(*allowed: UserRole):
    async def checker(user: CurrentUser) -> User:
        if user.role not in allowed:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "wow")
        return user
    return checker

CurrentAdmin = Annotated[User, Depends(require_role(UserRole.ADMIN))]


def get_admin_service(user_repo: UserRepositoryDep) -> AdminService:
    return AdminService(user_repo)

AdminServiceDep = Annotated[AdminService, Depends(get_admin_service)]