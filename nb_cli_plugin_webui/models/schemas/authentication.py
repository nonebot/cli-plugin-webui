from pydantic import BaseModel


class IsAvailableResponse(BaseModel):
    detail: str
