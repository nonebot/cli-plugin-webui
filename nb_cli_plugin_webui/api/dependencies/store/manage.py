import re
import math
from datetime import datetime, timezone, timedelta
from typing import List, Generic, Literal, TypeVar, Optional

from dateutil import parser

from nb_cli_plugin_webui.utils import safe_list_get
from nb_cli_plugin_webui.models.schemas.project import NonebotProjectMeta
from nb_cli_plugin_webui.models.schemas.store import Driver, Plugin, Adapter

from .load import load_module_data

_T = TypeVar("_T", Plugin, Adapter, Driver)
VISIBLE_ITEMS = 12


class StoreManager(Generic[_T]):
    def __init__(
        self,
        *,
        module_type: Literal["plugin", "adapter", "driver"],
        visible_items: int = VISIBLE_ITEMS,
    ) -> None:
        self.module_type = module_type
        self.visible_items = visible_items
        self.items: List[_T] = list()
        self.page = int()
        self.search_result: List[_T] = list()

    async def load_item(self) -> None:
        self.items = await load_module_data(self.module_type)  # type: ignore

    def get_item(self, *, is_search: bool = False) -> List[_T]:
        if is_search:
            return self.search_result
        else:
            return self.items

    def get_max_page(self, *, is_search: bool = False) -> int:
        if is_search:
            return math.ceil(len(self.search_result) / self.visible_items)
        else:
            return math.ceil(len(self.items) / self.visible_items)

    def _generate_page_items(self, items: List[_T]) -> List[_T]:
        a = self.page * self.visible_items
        b = a + self.visible_items
        return items[a:b]

    def generate_page(
        self,
        project_info: Optional[NonebotProjectMeta] = None,
        *,
        page: int,
        is_search: bool = False,
    ) -> List[_T]:
        self.page = page
        max_page = self.get_max_page(is_search=is_search)
        if self.page > max_page:
            self.page = max_page
        elif self.page < 0:
            self.page = 0

        if is_search:
            page_items = self._generate_page_items(self.search_result)
        else:
            page_items = self._generate_page_items(self.items)

        if project_info is None:
            return page_items

        cache_list = page_items[:]
        for i in cache_list:
            i.is_download = False
            if isinstance(i, (Plugin, Adapter, Driver)):
                for item in getattr(project_info, i.__class__.__name__.lower() + "s"):
                    if i.module_name == item.module_name:
                        i.is_download = True
                        break

        return cache_list

    def search_item(self, project_info: NonebotProjectMeta, content: str) -> None:
        filters_pattern = r"(is:[^ ]+(?:\s+is:[^ ]+)*)"
        filter_pattern = r"is:([^ ]+)"

        def custom_filter() -> None:
            for i in self.items:
                if content in i.module_name:
                    result.append(i)
                elif content in i.name:
                    result.append(i)
                elif content in i.desc:
                    result.append(i)
                elif content in i.author:
                    result.append(i)
                elif i.project_link:
                    if content in i.project_link:
                        result.append(i)

        def remove_item(item: _T) -> None:
            try:
                result.remove(item)
            except ValueError:
                pass

        result: List[_T] = list()
        filters_match = re.search(filters_pattern, content)
        if filters_match is None:
            custom_filter()
        else:
            filters = filters_match.group(1)
            content = content.replace(filters, str(), 1).strip()

            custom_filter()

            filter_match = re.findall(filter_pattern, filters)
            if filter_match:
                cache_list = result[:]

                if "downloaded" in filter_match:
                    if isinstance(safe_list_get(self.items, 0, str()), Plugin):
                        result = project_info.plugins  # type: ignore
                    elif isinstance(safe_list_get(self.items, 0, str()), Adapter):
                        result = project_info.adapters  # type: ignore
                    elif isinstance(safe_list_get(self.items, 0, str()), Driver):
                        result = project_info.drivers  # type: ignore

                    if len(filter_match) == 1:
                        self.search_result = result
                        return

                for i in cache_list:
                    for f in filter_match:
                        if f == "official":
                            if not i.is_official:
                                remove_item(i)
                        if f == "valid":
                            if isinstance(i, Plugin):
                                if not i.valid:
                                    remove_item(i)
                        if f == "new":
                            if isinstance(i, Plugin):
                                latest_time = (
                                    datetime.now(timezone(timedelta(hours=8)))
                                    - timedelta(weeks=1)
                                ).timestamp()
                                update_time = parser.parse(i.time).timestamp()
                                if update_time < latest_time:
                                    remove_item(i)

        self.search_result = result


PLUGIN_MANAGER: StoreManager[Plugin] = StoreManager[Plugin](module_type="plugin")
ADAPTER_MANAGER: StoreManager[Adapter] = StoreManager[Adapter](module_type="adapter")
DRIVER_MANAGER: StoreManager[Driver] = StoreManager[Driver](module_type="driver")
