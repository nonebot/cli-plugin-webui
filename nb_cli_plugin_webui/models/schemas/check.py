from pydantic import BaseModel


class PathInCheck(BaseModel):
    path: str


class PathInResponse(BaseModel):
    is_exist: int
