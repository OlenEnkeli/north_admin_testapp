from datetime import datetime as dt

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models.enums import UserType, user_type_enum


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    fullname: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    user_type: Mapped[UserType] = mapped_column(user_type_enum, default=UserType.USER)
    created_at: Mapped[dt] = mapped_column(default=dt.now, server_default=func.current_timestamp())
