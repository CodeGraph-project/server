from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from app.core.security import security_handler

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token") # 임시 url


async def get_current_user(
        token: Annotated[str: Depends(oauth2_scheme)],
        session: AsyncSession
) -> dict: # 임시임. 유저 모델 들어감
    pass