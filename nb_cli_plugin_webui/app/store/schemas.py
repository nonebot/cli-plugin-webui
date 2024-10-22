from typing import List, Union

from pydantic import BaseModel

from nb_cli_plugin_webui.app.models.types import ModuleType
from nb_cli_plugin_webui.app.schemas import GenericResponse
from nb_cli_plugin_webui.app.models.base import Driver, Adapter
from nb_cli_plugin_webui.app.models.store import Plugin, SearchTag


class StoreListResponse(
    GenericResponse[Union[List[Plugin], List[Adapter], List[Driver]]]
):
    now_page: int
    total_page: int
    total_item: int


class SearchRequest(BaseModel):
    module_type: ModuleType
    tags: List[SearchTag] = list()
    content: str
