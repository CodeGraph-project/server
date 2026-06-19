from fastapi import APIRouter, Query
from app.domain.user.dependencies import CurrentUser, UserRepositoryDep, UserServiceDep
from app.domain.user.schemas import UserResponse, UserSearchItem

user_router = APIRouter(prefix="/user", tags=["user"])

# 지금 project, scrap쪽이 다 안된 상태여서, 일단 대충 틀만 짜둠. user 도메인 좀 많이 바뀔수도
# 그리고 보니까 user 테이블에 유저 깃허브 링크가 없더라. 나중에 마이그레이션해서 수정해야 할 듯

@user_router.get("/me", response_model=UserResponse)
async def get_me(user: CurrentUser):
    return user


@user_router.get("/search", response_model=list[UserSearchItem])
async def search_user(
        user: CurrentUser,
        service: UserServiceDep,
        q: str = Query(..., min_length=1, description="유저 검색어"),
):
    return await service.search_user(q)