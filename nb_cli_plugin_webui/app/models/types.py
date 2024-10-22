from enum import Enum


class ModuleType(str, Enum):
    MODULE = "module"
    PLUGIN = "plugin"
    ADAPTER = "adapter"
    DRIVER = "driver"


class SearchTag(str, Enum):
    OFFICIAL = "official"
    VALID = "valid"
    LATEST = "latest"
    DOWNLOADED = "downloaded"
    AUTHOR = "author"
    TAG = "tag"
