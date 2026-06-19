from app.domain.user.models import User
from app.domain.user.repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository): # project, scrap 레포 들어갈거임
        self.user_repo = user_repo

    async def get_me(self, user_id: int) -> User:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            pass
        return user

    async def search_user(self, q: str) -> list[User]:
        q = q.strip()
        if not q:
            return []
        return await self.user_repo.search_by_username(q)

    async def my_page(self, user_id: int): # project, scrap 레포에서 가져오는거 들어갈거임
        user = await self.get_me(user_id)
        pass