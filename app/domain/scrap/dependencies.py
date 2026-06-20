from typing import Annotated
from fastapi import Depends
from app.core.database import AsyncSessionDep
from app.domain.scrap.repository import ScrapRepository


def get_scrap_repository(session: AsyncSessionDep) -> ScrapRepository:
    return ScrapRepository(session)

GetScrapRepository = Annotated[ScrapRepository, Depends(get_scrap_repository)]