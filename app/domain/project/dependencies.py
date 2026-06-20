from typing import Annotated
from fastapi import Depends
from app.core.database import AsyncSessionDep
from app.domain.project.repository import ProjectRepository


def get_project_repository(session: AsyncSessionDep) -> ProjectRepository:
    return ProjectRepository(session)

GetProjectRepository = Annotated[ProjectRepository, Depends(get_project_repository)]