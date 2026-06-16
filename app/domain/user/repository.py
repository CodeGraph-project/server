from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.domain.user.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_github_id(self, github_id: int) -> User | None:
        result = await self.session.exec(
            select(User)
            .where(User.github_id == github_id)
        )
        user = result.first()
        return user

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user