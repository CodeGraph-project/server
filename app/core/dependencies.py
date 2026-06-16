from fastapi import Depends
from typing import Annotated
from sqlmodel import select
from fastapi.security import OAuth2PasswordBearer
from app.core.database import AsyncSessionDep
from app.core.security import security_handler
from app.domain.user.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token") # 임시 url


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSessionDep
) -> User:
    payload = security_handler.decode_token(token)
    if payload.get("type") != "access":
        pass
    result = await session.exec(select(User).where(User.github_id == payload["github_id"]))
    user = result.first()
    if not user:
        pass
    return user

GetCurrentUser = Annotated[User, Depends(get_current_user)]