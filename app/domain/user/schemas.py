from pydantic import BaseModel
from app.domain.user.models import UserRole


class UserResponse(BaseModel):
    id: int
    github_id: int
    username: str
    avatar_url: str | None
    role: UserRole

    model_config = {"from_attributes": True}


class UserSearchItem(BaseModel):
    id: int
    username: str
    avatar_url: str | None

    model_config = {"from_attributes": True}