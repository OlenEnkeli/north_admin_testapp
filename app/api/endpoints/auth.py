from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_session, get_auth_user
from app.core.auth import JWTTokens, create_jwt_tokens
from app.models.user import User
from app.schemas.user import (
    UserCreateSchema,
    UserLoginSchema,
    UserReturnSchema,
    UserUpdateSchema,
)
from app.cruds.user import user_crud


router = APIRouter(tags=['Auth'])


@router.post(
    path='/users',
    description='Sign-up method',
    response_model=UserReturnSchema,
)
async def sign_up(
    origin: UserCreateSchema,
    session: AsyncSession = Depends(get_async_session),
) -> User:
    user: User = await user_crud.create(
        session=session,
        origin=origin,
    )
    if not user:
        raise HTTPException(
            status_code=400,
            detail='Can`t create user',
        )

    return user


@router.get(
    path='/users/current',
    description='Get current user profile',
    response_model=UserReturnSchema,
)
async def get_current_user(
    user: User = Depends(get_auth_user),
) -> User:
    return user


@router.patch(
    path='/users/current',
    description='Update current user profile',
    response_model=UserReturnSchema,
)
async def update_current_user(
    origin: UserUpdateSchema,
    user: User = Depends(get_auth_user),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    user: User = await user_crud.update(
        session=session,
        model_id=user.id,
        origin=origin,
    )
    if not user:
        raise HTTPException(
            status_code=400,
            detail='Can`t update user',
        )

    return user


@router.post(
    path='/login',
    description='User login',
    response_model=JWTTokens,
)
async def login(
    origin: UserLoginSchema,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> JWTTokens:
    user = await user_crud.login(
        session=session,
        email=origin.email,
        password=origin.password,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail={
                'Unauthorized': 'wrong email or password',
            },
        )

    return create_jwt_tokens(user_id=user.id)
