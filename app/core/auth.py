import hashlib

from datetime import datetime as dt
from datetime import timedelta as td

import jwt

from pydantic import BaseModel

from app.core.config import settings


class JWTTokens(BaseModel):
    access_token: str
    refresh_token: str


def dt_to_int(datetime: dt):
    return int(datetime.timestamp())


def create_jwt_tokens(
    user_id: int,
    expired_at: dt | None = None,
) -> JWTTokens:
    access_token_data = {
        'user_id': user_id,
        'type': 'access',
        'expired_at': dt_to_int(expired_at) if expired_at else None,
    }

    access_token = jwt.encode(
        payload=access_token_data,
        key=settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm,
    )

    refresh_token_data = {
        'user_id': user_id,
        'access_token': access_token,
        'type': 'refresh',
    }

    refresh_token = jwt.encode(
        payload=refresh_token_data,
        key=settings.jwt.secret_key,
        algorithm='HS256',
    )

    return JWTTokens(
        access_token=access_token,
        refresh_token=refresh_token,
    )


def validate_access_token(
    access_token: str,
) -> str | None:
    """ Возвращает user_id """

    payload: dict

    try:
        payload = jwt.decode(
            jwt=access_token,
            key=settings.jwt.secret_key,
            algorithms=settings.jwt.algorithm,
        )
    except jwt.DecodeError:
        return None

    if (
        'user_id' not in payload.keys() or
        'type' not in payload.keys() or
        'expired_at' not in payload.keys()
    ):
        return None

    if payload['type'] != 'access':
        return None

    if payload['expired_at'] and payload['expired_at'] <= dt_to_int(dt.now()):
        return None

    return payload['user_id']


def apply_refresh_token(
    refresh_token: str,
    expired_timedelta: td = td(days=30),
) -> JWTTokens | None:
    payload: dict

    try:
        payload = jwt.decode(
            jwt=refresh_token,
            key=settings.jwt.secret_key,
            algorithms=settings.jwt.algorithm,
        )
    except jwt.DecodeError:
        return None

    if (
        'user_id' not in payload.keys() or
        'access_token' not in payload.keys() or
        'type' not in payload.keys()
    ):
        return None

    if payload['type'] != 'refresh':
        return None

    return create_jwt_tokens(
        user_id=payload['user_id'],
        expired_at=dt.now() + expired_timedelta,
    )


def generate_password_hash(password: str) -> str:
    salted_password = f'{password}{settings.jwt.secret_key}'
    return hashlib.sha256(
        salted_password.encode(encoding='UTF-8')
    ).hexdigest()
