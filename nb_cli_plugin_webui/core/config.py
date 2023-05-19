from pathlib import Path

from nb_cli_plugin_webui import PLUGIN_NAME
from nb_cli_plugin_webui.models.app.config import WebUIConfig
from nb_cli_plugin_webui.utils.localstore import get_config_file

CONFIG_PATH = get_config_file(PLUGIN_NAME, "webui-config.json")


class Config:
    def __init__(self, config_file: Path):
        self.config_file = config_file

    @property
    def exist(self) -> bool:
        return CONFIG_PATH.is_file()

    def read(self) -> WebUIConfig:
        return WebUIConfig.parse_file(self.config_file)

    def store(self, data: WebUIConfig) -> None:
        CONFIG_PATH.write_text(data.to_json(), encoding="utf-8")


config = Config(CONFIG_PATH)
