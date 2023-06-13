from pydantic import BaseModel

from nb_cli_plugin_webui.utils.security import salt
from nb_cli_plugin_webui.core.configs.config import config


class LoginData(BaseModel):
    token: str
    mark: str

    def check_token(self) -> bool:
        conf = config.read()
        return salt.verify_token(
            conf.salt.get_secret_value() + self.token,
            conf.hashed_token,
        )


class LoginResponse(BaseModel):
    jwt_token: str


class IsAvailableResponse(BaseModel):
    detail: str
