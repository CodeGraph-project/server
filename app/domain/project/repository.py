from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.domain.project.models import Project, ProjectMember


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

        # 프로젝트 관련 메서드 추가 예정
        # 지금은 user 도메인에 필요한 기능만 추가

    async def count_owned_by(self, user_id: int) -> int:
        result = await self.session.exec(
            select(func.count()).select_from(Project).where(Project.owner_id == user_id)
        )
        return result.first()

    async def count_joined_by(self, user_id: int) -> int:
        result = await self.session.exec(
            select(func.count()).select_from(ProjectMember).where(Project.user_id == user_id)
        )
        return result.first()