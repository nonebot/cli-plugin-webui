import bcrypt
from passlib.context import CryptContext

token_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def gen_salt() -> str:
    return bcrypt.gensalt().decode()


def verify_token(plain_token: str, hashed_token: str) -> bool:
    return token_context.verify(plain_token, hashed_token)


def get_token_hash(token: str) -> str:
    return token_context.hash(token)
