import bcrypt
from pydantic import BaseModel
from passlib.context import CryptContext

token_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class NewToken(BaseModel):
    salt: str
    hashed_token: str


def gen_salt() -> str:
    return bcrypt.gensalt().decode()


def verify_token(plain_token: str, hashed_token: str) -> bool:
    return token_context.verify(plain_token, hashed_token)


def get_token_hash(token: str) -> str:
    return token_context.hash(token)


def reset_token(token: str) -> NewToken:
    salt = gen_salt()
    hashed_token = get_token_hash(salt + token)
    return NewToken(
        salt=salt,
        hashed_token=hashed_token,
    )
