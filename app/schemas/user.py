from typing import Annotated
from datetime import datetime as dt

from pydantic import AfterValidator

from app.core.auth import generate_password_hash
from app.models.enums import UserType
from app.schemas.base import BaseSchema


class UserUpdateSchema(BaseSchema):
    fullname: str
    password: Annotated[str, AfterValidator(generate_password_hash)]


class UserCreateSchema(UserUpdateSchema):
    email: str


class UserLoginSchema(BaseSchema):
    email: str
    password: Annotated[str, AfterValidator(generate_password_hash)]


class UserReturnSchema(BaseSchema):
    email: str
    fullname: str
    is_active: bool
    user_type: UserType
    created_at: dt
