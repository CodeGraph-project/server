from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.domain.user.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def get_by_github_id(self, github_id: int) -> User | None:
        result = await self.session.exec(
            select(User).where(User.github_id == github_id)
        )
        return result.first()

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user