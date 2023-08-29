from pydantic import BaseModel


class LogHistoryResponse(BaseModel):
    detail: list
