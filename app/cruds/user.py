from pydantic import BaseModel
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import UserType
from app.models.user import User
from app.schemas.user import UserCreateSchema
from app.cruds.base import BaseCRUD


class UserCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(model=User)

    @staticmethod
    def list_query() -> Select:
        return (
            select(User)
            .filter(User.user_type == UserType.USER)
            .filter(User.is_active.is_(True))
        )

    async def get_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> User | None:
        query = (
            select(User)
            .filter(User.email == email)
            .filter(User.is_active.is_(True))
        )

        return await session.scalar(query)

    async def create(
        self,
        session: AsyncSession,
        origin: UserCreateSchema,
        user_type: UserType = UserType.USER,
        **kwargs,
    ) -> User | None:
        return await super().create(
            session=session,
            origin=origin,
            user_type=user_type,
            **kwargs
        )

    async def login(
        self,
        session: AsyncSession,
        email: str,
        password: str,
    ) -> User | None:
        query = (
            select(User)
            .filter(User.email == email)
            .filter(User.password == password)
        )

        return await session.scalar(query)


user_crud = UserCRUD()
