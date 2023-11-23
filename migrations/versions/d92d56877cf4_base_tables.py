from datetime import datetime as dt
from enum import Enum
from typing import Sequence

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import ENUM, ARRAY


from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'd92d56877cf4'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


class UserType(str, Enum):
    USER = 'user'
    ADMIN = 'admin'
    ROOT = 'root'


def upgrade() -> None:
    user_type_enum = ENUM(UserType, name='user_type', create_type=True)

    op.create_table(
        'users',
        Column('id', Integer, primary_key=True),
        Column('email', String, unique=True, nullable=False, index=True),
        Column('password', String, nullable=False),
        Column('fullname',  String, nullable=True),
        Column('is_active', Boolean, default=True),
        Column('user_type', user_type_enum, default=UserType.USER),
        Column('created_at', DateTime, default=dt.now, server_default=func.current_timestamp()),
    )

    op.create_table(
        'posts',
        Column('id', Integer, primary_key=True),
        Column('text', String, nullable=False),
        Column('tags', ARRAY(String), nullable=True),
        Column('is_published', Boolean, default=True),
        Column('author_id', Integer, ForeignKey('users.id'), index=True),
        Column('created_at', DateTime, default=dt.now, server_default=func.current_timestamp()),
    )


def downgrade() -> None:
    op.drop_table('posts')
    op.drop_table('users')
    op.execute('DROP TYPE user_type;')
