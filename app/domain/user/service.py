from app.domain.user.models import User
from app.domain.user.repository import UserRepository
from app.domain.project.repository import ProjectRepository
from app.domain.scrap.repository import ScrapRepository
from app.domain.user.schemas import UserStats


class UserService:
    def __init__(
            self,
            user_repo: UserRepository,
            project_repo: ProjectRepository,
            scrap_repo: ScrapRepository,
    ):
        self.user_repo = user_repo
        self.project_repo = project_repo
        self.scrap_repo = scrap_repo

    async def search_user(self, q: str, exclude_ids: list[int] | None = None) -> list[User]:
        q = q.strip()
        if not q:
            return []
        return await self.user_repo.search_by_username(q, exclude_ids)

    async def get_stats(self, user_id: int) -> UserStats:
        return UserStats(
            owned_project=await self.project_repo.count_owned_by(user_id),
            joined_project=await self.project_repo.count_joined_by(user_id),
            scraps=await self.scrap_repo.count_by_user(user_id),
        )