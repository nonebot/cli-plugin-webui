from enum import Enum
from typing import Any, List, Union

from pydantic import BaseModel

from nb_cli_plugin_webui.app.schemas import GenericResponse
from nb_cli_plugin_webui.app.constants import ModuleType as BaseModuleType


class ConfigType(str, Enum):
    project = "project"
    toml = "toml"


ConfigModuleType = Union[BaseModuleType, ConfigType]


class ModuleConfigSimpleInfo(BaseModel):
    title: str
    description: str
    name: str


class ModuleConfigChild(ModuleConfigSimpleInfo):
    default: Any
    conf_type: str
    enum: List[Any]
    configured: Any
    is_secret: bool
    latest_change: str = str()


class ModuleConfigFather(ModuleConfigSimpleInfo):
    module_type: ConfigModuleType
    properties: List[ModuleConfigChild]


class ModuleConfigUpdateRequest(BaseModel):
    env: str
    conf_type: str
    k: str
    v: Any


class ModuleConfigResponse(GenericResponse[List[ModuleConfigFather]]):
    pass
