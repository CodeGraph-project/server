from fastapi import APIRouter
from app.domain.admin.dependencies import CurrentAdmin
from app.domain.user.schemas import UserSearchItem, RoleUpdateRequest
from app.domain.admin.dependencies import AdminServiceDep

admin_router = APIRouter(prefix="/admin", tags=["admin"])


@admin_router.patch("/users/{user_id}/role", response_model=UserSearchItem)
async def change_user_role(
    user_id: int,
    body: RoleUpdateRequest,
    admin: CurrentAdmin,
    service: AdminServiceDep,
):
    return await service.change_user_role(user_id, body.role)