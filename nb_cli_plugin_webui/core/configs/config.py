from pathlib import Path
from typing import Union

import click
from pydantic import ValidationError

from nb_cli_plugin_webui.utils.store import get_config_file
from nb_cli_plugin_webui.models.domain.config import WebUIConfig

CONFIG_PATH = get_config_file("config.json")
CONFIG_CACHE: Union[WebUIConfig, None] = None


class Config:
    def __init__(self, config_file: Path):
        self.config_file = config_file

    @property
    def exist(self) -> bool:
        return CONFIG_PATH.is_file()

    def read(self, refresh: bool = False) -> WebUIConfig:
        global CONFIG_CACHE
        if not CONFIG_CACHE or refresh:
            try:
                CONFIG_CACHE = WebUIConfig.parse_file(self.config_file)
            except ValidationError as err:
                click.secho(f"Config file is invalid: {err}", fg="red")
                click.secho(
                    "Enter this try to fix: nb ui clear",
                    fg="yellow",
                )
                exit(-1)
        return CONFIG_CACHE

    def store(self, data: WebUIConfig) -> None:
        CONFIG_PATH.write_text(data.to_json(), encoding="utf-8")


config = Config(CONFIG_PATH)
