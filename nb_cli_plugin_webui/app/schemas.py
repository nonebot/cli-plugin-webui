from typing import List, Generic, TypeVar, Optional

from pydantic import BaseModel
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class GenericResponse(GenericModel, Generic[DataT]):
    detail: DataT


class ModuleTag(BaseModel):
    label: str
    color: str


class ModuleInfo(BaseModel):
    module_name: str
    project_link: str
    name: str
    desc: str
    author: str
    homepage: str
    tags: Optional[List[ModuleTag]]
    is_official: bool

    is_download: Optional[bool]


class Plugin(ModuleInfo):
    type: Optional[str]
    supported_adapters: Optional[List[str]]
    valid: bool
    version: str
    time: str
    skip_test: bool

    # WebUI private field
    config_detail: dict = dict()

    class Config:
        module_name = "plugins"


class Adapter(ModuleInfo):
    pass

    class Config:
        module_name = "adapters"


class Driver(ModuleInfo):
    pass

    class Config:
        module_name = "drivers"


class NoneBotProjectMeta(BaseModel):
    project_id: str
    project_name: str
    project_dir: str
    mirror_url: str
    adapters: List[ModuleInfo]
    drivers: List[ModuleInfo]
    plugins: List[Plugin]
    plugin_dirs: List[str]
    builtin_plugins: List[str]

    is_running: bool = False

    use_run_script: bool = False
    run_script_name: str = "bot.py"
