from typing import Type

from loguru import logger
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base


class BaseCRUD:
    model: Type[Base]

    def __init__(self, model: Type[Base]):
        self.model = model

    async def get_all(self, session: AsyncSession) -> list[Base]:
        query = select(self.model)
        return list(await session.scalars(query))

    async def get_by_id(
        self,
        session: AsyncSession,
        model_id: str | int,
    ) -> Base | None:
        query = select(self.model).filter(self.model.id == model_id)
        return await session.scalar(query)

    async def remove_by_id(
        self,
        session: AsyncSession,
        model_id: str | int,
    ) -> bool:
        query = delete(self.model).filter(self.model.id == model_id)
        result = await session.execute(query)
        return result.rowcount == 1

    async def create(
        self,
        session: AsyncSession,
        origin: BaseModel | None = None,
        **kwargs,
    ) -> Base | None:
        if origin:
            db_object = self.model(**origin.model_dump())
        else:
            db_object = self.model(**kwargs)

        try:
            session.add(db_object)
            await session.commit()
            await session.refresh(db_object)
            return db_object
        except (IntegrityError, DatabaseError) as e:
            logger.info(f'Can`t save object to DB: {str(e)} ')
            return None

    async def update(
        self,
        session: AsyncSession,
        model_id: str | int,
        origin: BaseModel,
    ) -> Base | None:
        db_object = await self.get_by_id(
            session=session,
            model_id=model_id,
        )
        if not db_object:
            return None

        for key, value in origin.model_dump().items():
            setattr(db_object, key, value)

        try:
            await session.merge(db_object)
            await session.commit()
            await session.refresh(db_object)
            return db_object
        except (IntegrityError, DatabaseError) as e:
            logger.info(f'Can`t save/update object to DB: {str(e)} ')
            return None
