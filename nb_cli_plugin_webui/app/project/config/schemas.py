from enum import Enum
from typing import Any, List, Union, Optional

from pydantic import BaseModel

from nb_cli_plugin_webui.app.schemas import GenericResponse
from nb_cli_plugin_webui.app.models.types import ModuleType as BaseModuleType


class ConfigType(str, Enum):
    PROJECT = "project"
    TOML = "toml"


ConfigModuleType = Union[BaseModuleType, ConfigType]


class ModuleConfigSimpleInfo(BaseModel):
    title: str
    description: Optional[str]
    name: str


class Item(BaseModel):
    enum: Optional[List[Any]]
    type: str


class ModuleConfigChild(ModuleConfigSimpleInfo):
    default: Any
    conf_type: str
    enum: Optional[List[Any]]
    configured: Any
    items: Optional[Item]
    unique_items: bool
    is_secret: bool
    latest_change: str = ".env"


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
