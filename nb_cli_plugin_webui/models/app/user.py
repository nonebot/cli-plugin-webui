from pydantic import BaseModel

from nb_cli_plugin_webui.utils.security import salt


class User(BaseModel):
    token: str


class UserInDB(User):
    salt: str = str()
    hashed_token: str = str()

    def check_token(self, token: str) -> bool:
        return salt.verify_token(self.salt + token, self.hashed_token)

    def change_token(self, token: str) -> None:
        self.salt = salt.gen_salt()
        self.hashed_token = salt.get_token_hash(token)
