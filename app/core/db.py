from datetime import datetime as dt

from sqlalchemy import func
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import QueuePool

from app.core.config import settings


engine = create_async_engine(
    settings.postgres.postgres_url,
    echo=False,
    pool_size=10,
    poolclass=QueuePool,
    pool_pre_ping=True,
    pool_recycle=3600,
)
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


class Base(AsyncAttrs, DeclarativeBase):
    pass
