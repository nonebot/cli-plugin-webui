from typing import Dict, List, Optional

from pydantic import BaseModel
from nb_cli.config import Driver, Adapter, SimpleInfo


class NonebotProjectMeta(BaseModel):
    project_id: str
    project_name: str
    project_dir: str
    mirror_url: str
    adapters: List[SimpleInfo]
    drivers: List[SimpleInfo]
    plugins: List[str]
    plugin_dirs: List[str]
    builtin_plugins: List[str]


class NonebotProjectList(BaseModel):
    projects: Dict[str, Optional[NonebotProjectMeta]]


class CreateProjectData(BaseModel):
    project_name: str
    project_dir: str
    mirror_url: str
    driver: Driver
    adapter: Adapter


class CreateProjectResponse(BaseModel):
    log_key: str


class ProjectListResponse(NonebotProjectList):
    ...


class DeleteProjectResponse(BaseModel):
    project_id: str
