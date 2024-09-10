from enum import Enum


class ModuleType(str, Enum):
    plugin = "plugin"
    adapter = "adapter"
    driver = "driver"


class SearchTag(str, Enum):
    official = "official"
    valid = "valid"
    latest = "latest"
    downloaded = "downloaded"
    author = "author"
    tag = "tag"
