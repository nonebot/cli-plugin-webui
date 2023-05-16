from pydantic import BaseModel, SecretStr


class ServerConfig(BaseModel):
    host: str
    port: str


class WebUIConfig(BaseModel):
    token: SecretStr
    secret_key: SecretStr
    is_customize: bool
    server: ServerConfig
