from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel

from .types import ModuleType
from .base import Plugin as BasePlugin
from .types import SearchTag as SearchTagEnum
from .base import ModuleInfo as BaseModuleInfo
from .base import NoneBotProjectMeta as BaseNoneBotProjectMeta


class PluginType(str, Enum):
    """
    类型参考:
    - https://github.com/nonebot/noneflow/blob/main/src/utils/validation/constants.py#L17
    """

    APPLICATION = "application"
    LIBRARY = "library"


class Plugin(BasePlugin):
    """
    结构参考:
    - https://github.com/nonebot/noneflow/blob/main/src/utils/store_test/models.py#L14
    """

    type: Optional[PluginType]
    supported_adapters: Optional[list[str]]
    valid: bool
    time: str
    version: str
    skip_test: bool

    module_type: Literal["plugin"] = ModuleType.PLUGIN


class ModuleInfo(BaseModuleInfo):
    module_type: Literal["module"] = ModuleType.MODULE


class NoneBotProjectMeta(BaseNoneBotProjectMeta[Plugin]):
    pass


class SearchTag(BaseModel):
    label: SearchTagEnum
    text: str = str()
