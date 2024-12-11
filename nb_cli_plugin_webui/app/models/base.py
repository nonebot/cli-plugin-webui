from typing import Any, Dict, List, Generic, TypeVar, Optional

from pydantic import Field, BaseModel, validator


class ModuleTag(BaseModel):
    label: str
    color: str


class ModuleInfo(BaseModel):
    module_name: str = "unknown"
    project_link: str = "unknown"
    name: str = "unknown"
    desc: str = "unknown"
    author: str = "unknown"
    homepage: str = "unknown"

    # nonebot:PluginMetadata 类型, 为通用移至此处
    usage: str = "unknown"
    extra: Dict[Any, Any] = Field(default_factory=dict)

    # noneflow:PublishInfo 类型, 为通用移至此处
    tags: Optional[List[ModuleTag]]
    is_official: bool = False
    version: str = "0.0.0"

    # WebUI 拓展类型
    is_download: bool = False

    @validator("project_link", pre=True, always=True)
    def set_project_link_default(cls, v):
        return v if v is not None else "unknown"

    @validator("author", pre=True, always=True)
    def set_author_default(cls, v):
        return v if v is not None else "unknown"

    @validator("homepage", pre=True, always=True)
    def set_homepage_default(cls, v):
        return v if v is not None else "unknown"


class Plugin(ModuleInfo):
    config: dict = dict()

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


_T = TypeVar("_T", bound=Plugin)


class NoneBotProjectMeta(BaseModel, Generic[_T]):
    project_id: str
    project_name: str
    project_dir: str
    mirror_url: str
    adapters: List[ModuleInfo]
    drivers: List[ModuleInfo]
    plugins: List[_T]
    plugin_dirs: List[str]
    builtin_plugins: List[str]

    is_running: bool = False

    use_env: str = ".env"
    use_run_script: bool = False
    run_script_name: str = "bot.py"
