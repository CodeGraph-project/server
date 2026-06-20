from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.domain.scrap.models import Scrap


class ScrapRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # 스크랩 관련 메서드 추가 예정
    # 지금은 user 도메인에 필요한 기능만 추가

    async def count_by_user(self, user_id: int) -> int:
        result = await self.session.exec(
            select(func.count().select_from(Scrap).where(Scrap.user_id == user_id))
        )
        return result.first()