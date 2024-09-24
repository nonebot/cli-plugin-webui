from pydantic import BaseModel


class LoginRequest(BaseModel):
    token: str
    mark: str


class VerifyRequest(BaseModel):
    jwt_token: str
