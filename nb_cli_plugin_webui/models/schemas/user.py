from pydantic import BaseModel

from nb_cli_plugin_webui.config import config
from nb_cli_plugin_webui.utils.security import salt


class UserInLogin(BaseModel):
    token: str
    string: str

    def check_token(self) -> bool:
        conf = config.read()
        return salt.verify_token(
            conf.salt.get_secret_value() + self.token,
            conf.hashed_token,
        )


class UserWithJWT(BaseModel):
    jwt_token: str


class UserInResponse(BaseModel):
    user: UserWithJWT
