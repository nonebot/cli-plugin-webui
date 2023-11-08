from typing import Dict, List

from pydantic import BaseModel

from nb_cli_plugin_webui.app.schemas import (
    ModuleInfo,
    GenericResponse,
    NoneBotProjectMeta,
)


class ProjectTomlDetail(BaseModel):
    project_name: str
    adapters: List[Dict[str, str]]
    plugins: List[str]
    plugin_dirs: List[str]
    builtin_plugins: List[str]


class CreateProjectData(BaseModel):
    is_bootstrap: bool
    project_name: str
    project_dir: str
    mirror_url: str
    drivers: List[ModuleInfo]
    adapters: List[ModuleInfo]
    use_src: bool


class AddProjectData(BaseModel):
    project_name: str
    project_dir: str
    mirror_url: str
    adapters: List[str] = list()
    plugins: List[str] = list()
    plugin_dirs: List[str] = list()
    builtin_plugins: List[str] = list()


class ListProjectResponse(GenericResponse[Dict[str, NoneBotProjectMeta]]):
    pass


class CheckProjectTomlResponse(GenericResponse[ProjectTomlDetail]):
    msg: str
    level: str
