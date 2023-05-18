import json
from typing import Any

from pydantic import BaseModel, SecretStr

from nb_cli_plugin_webui.utils.security import salt


class SecretStrJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, SecretStr):
            return o.get_secret_value()
        return super().default(o)


class ServerConfig(BaseModel):
    host: str
    port: str


class WebUIConfig(BaseModel):
    token: SecretStr
    hashed_token: str = str()
    salt: SecretStr = SecretStr(str())
    secret_key: SecretStr
    is_customize: bool
    server: ServerConfig = ServerConfig(host="localhost", port="12345")

    def to_json(self):
        return json.dumps(self.dict(), cls=SecretStrJSONEncoder)

    def check_token(self):
        return salt.verify_token(
            self.salt.get_secret_value() + self.token.get_secret_value(),
            self.hashed_token,
        )

    def reset_token(self):
        self.salt = SecretStr(salt.gen_salt())
        self.hashed_token = salt.get_token_hash(self.token.get_secret_value())
