from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.domain.user.models import UserRole


class UserSearchItem(BaseModel):
    id: int
    username: str
    avatar_url: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserStats(BaseModel):
    owned_projects: int
    joined_projects: int
    scraps: int


class MyProfileResponse(BaseModel):
    id: int
    github_id: int
    username: str
    avatar_url: str
    role: UserRole
    created_at: datetime
    stats: UserStats

    model_config = ConfigDict(from_attributes=True)

class RoleUpdateRequest(BaseModel):
    role: UserRole