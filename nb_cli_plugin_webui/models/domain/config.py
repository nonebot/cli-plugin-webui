import json
from typing import Any, Dict

from pydantic import BaseModel, SecretStr

from nb_cli_plugin_webui.utils.security import salt


class SecretStrJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, SecretStr):
            return o.get_secret_value()
        return super().default(o)


class ServerConfig(BaseModel):
    host: str = "localhost"
    port: str = "12345"
    debug: bool = False

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
        }


class WebUIConfig(ServerConfig):
    hashed_token: str = str()
    salt: SecretStr = SecretStr(str())
    secret_key: SecretStr
    base_dir: str

    def to_json(self) -> str:
        return json.dumps(self.dict(), cls=SecretStrJSONEncoder)

    def reset_token(self, token: str) -> None:
        self.salt = SecretStr(salt.gen_salt())
        self.hashed_token = salt.get_token_hash(self.salt.get_secret_value() + token)
