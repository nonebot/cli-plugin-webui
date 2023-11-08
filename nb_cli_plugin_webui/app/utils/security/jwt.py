from typing import Dict
from datetime import datetime, timedelta

import jwt
from pydantic import ValidationError

from .schemas import JWTMeta

JWT_SUBJECT: str = "access"
ALGORITHM: str = "HS256"
EXPIRE_SECONDS: int = 60 * 60 * 24


def create_jwt(
    payload: Dict[str, str], secret_key: str, expire_seconds: timedelta
) -> str:
    to_encode = payload.copy()
    expire = datetime.utcnow() + expire_seconds
    to_encode.update(JWTMeta(exp=expire, sub=JWT_SUBJECT).dict())
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)


def create_access_for_header(detail: str, secret_key: str) -> str:
    return create_jwt(
        payload={"token": detail},
        secret_key=secret_key,
        expire_seconds=timedelta(seconds=EXPIRE_SECONDS),
    )


def verify_and_read_jwt(token: str, secret_key: str) -> str:
    try:
        return jwt.decode(token, secret_key, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError as err:
        raise ValueError("Session(token) has expired.") from err
    except jwt.InvalidTokenError as err:
        raise ValueError("Invalid token.") from err
    except ValidationError as err:
        raise ValueError("Malformed payload in token.") from err
    except Exception as err:
        raise ValueError(f"Unknown error: {err}") from err
