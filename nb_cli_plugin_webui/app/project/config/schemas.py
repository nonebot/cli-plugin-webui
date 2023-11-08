from typing import Any, List

from pydantic import BaseModel

from nb_cli_plugin_webui.app.schemas import GenericResponse


class ModuleConfigSimpleInfo(BaseModel):
    title: str
    description: str
    name: str


class ModuleConfigChild(ModuleConfigSimpleInfo):
    default: Any
    item_type: str
    enum: List[Any]
    configured: Any
    latest_change: str = str()


class ModuleConfigFather(ModuleConfigSimpleInfo):
    properties: List[ModuleConfigChild]


class ModuleConfigUpdateRequest(BaseModel):
    env: str
    key_type: str
    k: str
    v: Any


class ModuleConfigResponse(GenericResponse[List[ModuleConfigFather]]):
    pass
