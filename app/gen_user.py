import asyncio

from app.models.user import User, UserType
from app.core.db import async_session


async def gen_users() -> None:
    async with async_session() as session:
        for i in range(0,1000):
            user = User(
                email=f'email-{i}@test.app',
                fullname=f'Full Name {i}',
                password='Fake',
                is_active=True,
                user_type=UserType.USER,
            )
            session.add(user)
        await session.commit()


if __name__ == '__main__':
    asyncio.run(gen_users())