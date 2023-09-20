from typing import List, Optional

from pydantic import BaseModel


class Tag(BaseModel):
    label: str
    color: str


class SimpleInfo(BaseModel):
    module_name: str
    project_link: str
    name: str
    desc: str
    author: str
    homepage: str
    tags: Optional[List[Tag]]
    is_official: bool
    is_download: Optional[bool]


class Plugin(SimpleInfo):
    type: Optional[str]
    supported_adapters: Optional[List[str]]
    valid: bool
    version: str
    time: str
    skip_test: bool

    class Config:
        module_name = "plugins"


class Adapter(SimpleInfo):
    ...

    class Config:
        module_name = "adapters"


class Driver(SimpleInfo):
    ...

    class Config:
        module_name = "drivers"


class StoreListResponse(BaseModel):
    now_page: int
    total_page: int
    total_item: int
    data: list


class StoreSearchRequest(BaseModel):
    project_id: str
    module_type: str
    content: str
