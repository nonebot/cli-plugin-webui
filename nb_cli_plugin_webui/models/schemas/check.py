from pydantic import BaseModel


class PathCheckInResponse(BaseModel):
    is_exist: int
