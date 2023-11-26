
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from north_admin import NorthAdmin, AuthProvider, UserReturnSchema
from north_admin.types import ModelType

from app.models.user import User, UserType
from app.core.config import settings

from .routes.user import router as user_admin_router


class AdminAuthProvider(AuthProvider):
    async def login(
        self,
        session: AsyncSession,
        login: str,
        password: str,
    ) -> ModelType | None:
        query = (
            select(User)
            .filter(User.email == login)
            .filter(User.user_type.in_([UserType.ROOT, UserType.ADMIN]))
        )

        return await session.scalar(query)

    async def get_user_by_id(
        self,
        session: AsyncSession,
        user_id: int | str,
    ) -> ModelType | None:
        query = (
            select(User)
            .filter(User.id == user_id)
            .filter(User.user_type.in_([UserType.ROOT, UserType.ADMIN]))
        )

        return await session.scalar(query)

    async def to_user_scheme(
        self,
        user: User,
    ) -> UserReturnSchema:
        return UserReturnSchema(
            id=user.id,
            login=user.email,
            fullname=user.fullname,
        )


admin_app = NorthAdmin(
    sqlalchemy_uri=settings.postgres.postgres_url,
    jwt_secket_key=settings.jwt.secret_key,
    auth_provider=AdminAuthProvider,
)

admin_app.add_admin_routes(user_admin_router)