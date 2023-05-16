from pydantic import BaseModel


class WebsocketAuthorizationData(BaseModel):
    cookie: str
