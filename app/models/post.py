from datetime import datetime as dt

from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from app.core.db import Base
from app.models.user import User


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    text: Mapped[str] = mapped_column(nullable=False)
    is_published: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[dt] = mapped_column(default=dt.now, server_default=func.current_timestamp())

    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    author: Mapped[User] = relationship(back_populates='posts')
