from typing import Any, List

from pydantic import BaseModel

from nb_cli_plugin_webui.app.constants import MODULE_TYPE
from nb_cli_plugin_webui.app.schemas import GenericResponse


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
    module_type: MODULE_TYPE
    properties: List[ModuleConfigChild]


class ModuleConfigUpdateRequest(BaseModel):
    env: str
    conf_type: str
    k: str
    v: Any


class ModuleConfigResponse(GenericResponse[List[ModuleConfigFather]]):
    pass
