from nb_cli_plugin_webui import PLUGIN_NAME
from nb_cli_plugin_webui.utils.localstore import get_config_file
from nb_cli_plugin_webui.models.schemas.config import WebUIConfig


class Config:
    CONFIG_PATH = get_config_file(PLUGIN_NAME, "webui-config.json")

    def __init__(self, conf: WebUIConfig):
        self.conf = conf

    @classmethod
    def exist(cls) -> bool:
        return cls.CONFIG_PATH.is_file()

    @classmethod
    def load(cls) -> WebUIConfig:
        return WebUIConfig.parse_file(cls.CONFIG_PATH, encoding="utf-8")

    def store(self) -> None:
        self.CONFIG_PATH.write_text(self.conf.to_json(), encoding="utf-8")
