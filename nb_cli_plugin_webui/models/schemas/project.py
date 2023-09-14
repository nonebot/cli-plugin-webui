from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel

from nb_cli_plugin_webui.models.schemas.store import Driver
from nb_cli_plugin_webui.models.schemas.store import Adapter, SimpleInfo
from nb_cli_plugin_webui.models.schemas.store import Plugin as BasePlugin


class Plugin(BasePlugin):
    config_detail: dict = dict()


class NonebotProjectMeta(BaseModel):
    project_id: str
    project_name: str
    project_dir: str
    mirror_url: str
    adapters: List[SimpleInfo]
    drivers: List[SimpleInfo]
    plugins: List[Plugin]
    plugin_dirs: List[str]
    builtin_plugins: List[str]

    is_running: bool = False

    use_run_script: bool = False
    run_script_name: str = "bot.py"


class NonebotProjectList(BaseModel):
    projects: Dict[str, NonebotProjectMeta]


class CreateProjectData(BaseModel):
    is_bootstrap: bool
    project_name: str
    project_dir: str
    mirror_url: str
    drivers: List[Driver]
    adapters: List[Adapter]
    use_src: bool


class CreateProjectResponse(BaseModel):
    log_key: str


class AddProjectResponse(BaseModel):
    log_key: str


class ProjectListResponse(NonebotProjectList):
    ...


class DeleteProjectResponse(BaseModel):
    project_id: str


class InstallModuleResponse(BaseModel):
    log_key: str


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


class ModuleConfigResponse(BaseModel):
    detail: List[ModuleConfigFather]


class ModuleSettingRequest(BaseModel):
    env: str
    k_type: str
    k: str
    v: Any


class DotenvListResponse(BaseModel):
    detail: List[str]


class AddProjectData(BaseModel):
    project_name: str
    project_dir: str
    mirror_url: str
    adapters: List[str]
    plugins: List[str]
    plugin_dirs: List[str]
    builtin_plugins: List[str]


class CheckProjectTomlDetail(BaseModel):
    project_name: str
    adapters: List[Dict[str, str]]
    plugins: List[str]
    plugin_dirs: List[str]
    builtin_plugins: List[str]


class CheckProjectTomlResponse(BaseModel):
    is_pass: bool
    level: Literal["success", "warning", "error"]
    msg: str
    detail: Optional[CheckProjectTomlDetail] = None
