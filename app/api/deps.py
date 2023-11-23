from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import validate_access_token
from app.core.db import async_session
from app.models.enums import UserType
from app.models.user import User
from app.cruds.user import user_crud


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_auth_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    user_id = validate_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail='Wrong JWT Token')

    user = await user_crud.get_by_id(
        session=session,
        model_id=user_id,
    )
    if not user:
        raise HTTPException(status_code=401, detail='Wrong JWT Token')

    if not user.is_active:
        raise HTTPException(status_code=403, detail='User is blocked')

    return user


async def get_admin_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    """
    Проверка, что аутентифицированный пользователь является администратором.
    """
    user = await get_auth_user(session=session, token=token)
    if user.user_type not in (UserType.ADMIN, UserType.ROOT):
        raise HTTPException(status_code=403, detail='Admin user required')

    return user
