from enum import Enum

from sqlalchemy.dialects.postgresql import ENUM


class UserType(str, Enum):
    USER = 'user'
    ADMIN = 'admin'
    ROOT = 'root'


user_type_enum = ENUM(UserType, name='user_type')
