from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from app.domain.user.models import User
from app.domain.user.schemas import UserRole


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

    async def search_by_username(
            self, q: str, exclude_ids: list[int] | None = None, limit: int = 20
    ) -> list[User]:
        stmt = select(User).where(User.username.ilike(f"%{q}%"))
        if exclude_ids:
            stmt = stmt.where(User.id.notin_(exclude_ids))
        stmt = stmt.order_by(func.length(User.username)).limit(limit)
        result = await self.session.exec(stmt)
        return result.all()

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_role(self, user: User, role: UserRole) -> User:
        user.role = role
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user