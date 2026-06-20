from app.domain.user.models import User, UserRole
from app.domain.user.repository import UserRepository


class AdminService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def change_user_role(self, user_id: int, role: UserRole) -> User:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            pass
        return await self.user_repo.update_role(user, role)