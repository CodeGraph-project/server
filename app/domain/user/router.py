from fastapi import APIRouter, Query
from app.domain.user.dependencies import CurrentUser, UserServiceDep
from app.domain.user.schemas import UserSearchItem, MyProfileResponse

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/me", response_model=MyProfileResponse)
async def get_me(user: CurrentUser, service: UserServiceDep):
    stats = await service.get_stats(user.id)
    return MyProfileResponse(
        **user.model_dump(),
        stats=stats
    )


@user_router.get("/search", response_model=UserSearchItem)
async def search_user(
        user: CurrentUser,
        service: UserServiceDep,
        q: str = Query(..., min_length=1),
        exclude: list[int] = Query(default=[])
):
    return await service.search(q=q, exclude=exclude)