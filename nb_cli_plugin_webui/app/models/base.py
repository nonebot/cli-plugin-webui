from typing import Any, Dict, List, Generic, TypeVar, ClassVar, Optional

from pydantic import Field, BaseModel
from pydantic.functional_validators import field_validator


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
    tags: Optional[List[ModuleTag]] = None
    is_official: bool = False
    version: str = "0.0.0"

    # WebUI 拓展类型
    is_download: bool = False

    @field_validator("project_link", "author", "homepage", mode="before")
    @classmethod
    def set_default_if_none(cls, v):
        return v if v is not None else "unknown"


class Plugin(ModuleInfo):
    config: dict = dict()
    _registry_name: ClassVar[str] = "plugins"


class Adapter(ModuleInfo):
    _registry_name: ClassVar[str] = "adapters"


class Driver(ModuleInfo):
    _registry_name: ClassVar[str] = "drivers"


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
