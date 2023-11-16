import re
import math
from asyncio import create_task, as_completed
from datetime import datetime, timezone, timedelta
from typing import (
    TYPE_CHECKING,
    List,
    Union,
    Generic,
    Literal,
    TypeVar,
    Optional,
    overload,
)

import httpx
from nb_cli import cache
from dateutil import parser

from nb_cli_plugin_webui.i18n import _
from nb_cli_plugin_webui.app.config import Config
from nb_cli_plugin_webui.app.logging import logger as log
from nb_cli_plugin_webui.app.utils.list_utils import safe_list_get
from nb_cli_plugin_webui.app.schemas import Driver, Plugin, Adapter, NoneBotProjectMeta

_T = TypeVar("_T", Plugin, Adapter, Driver)
VISIBLE_ITEMS = Config.extension_store_visible_items

if TYPE_CHECKING:

    @overload
    async def load_module_data(module_type: Literal["plugin"]) -> List[Plugin]:
        ...

    @overload
    async def load_module_data(module_type: Literal["adapter"]) -> List[Adapter]:
        ...

    @overload
    async def load_module_data(module_type: Literal["driver"]) -> List[Driver]:
        ...

    async def load_module_data(
        module_type: Literal["plugin", "adapter", "driver"],
    ) -> Union[List[Plugin], List[Adapter], List[Driver]]:
        ...

else:

    @cache(ttl="5m")
    async def load_module_data(
        module_type: Literal["plugin", "adapter", "driver"],
    ) -> Union[List[Plugin], List[Adapter], List[Driver]]:
        if module_type == "plugin":
            module_class = Plugin
        elif module_type == "adapter":
            module_class = Adapter
        elif module_type == "driver":
            module_class = Driver
        else:
            raise ValueError(
                _("Invalid module type: {module_type}").format(module_type=module_type)
            )

        module_name: str = getattr(module_class.__config__, "module_name")
        exceptions: List[Exception] = list()
        urls = [
            f"https://registry.nonebot.dev/{module_name}.json",
            f"https://cdn.jsdelivr.net/gh/nonebot/registry@results/{module_name}.json",
            f"https://cdn.staticaly.io/gh/nonebot/registry@results/{module_name}.json",
            f"https://jsd.cdn.zzko.cn/gh/nonebot/registry@results/{module_name}.json",
            (
                "https://ghproxy.com/https://raw.githubusercontent.com/"
                + f"nonebot/registry/results/{module_name}.json"
            ),
        ]

        async def _request(url: str) -> httpx.Response:
            async with httpx.AsyncClient() as client:
                return await client.get(url)

        tasks = [create_task(_request(url)) for url in urls]
        for future in as_completed(tasks):
            try:
                resp = await future
                items = resp.json()
                result = [module_class.parse_obj(item) for item in items]
                for task in tasks:
                    if not task.done():
                        task.cancel()
                return result  # type: ignore
            except Exception as err:
                exceptions.append(err)

        log.error(
            f"Failed to get {module_name} list: {''.join([str(e) for e in exceptions])}"
        )


class ModuleStoreManager(Generic[_T]):
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
        self.items = await load_module_data(self.module_type) or list()  # type: ignore

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

    def generate_page(
        self,
        project_info: Optional[NoneBotProjectMeta] = None,
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

        def generate_page_items(items: List[_T]) -> List[_T]:
            a = self.page * self.visible_items
            b = a + self.visible_items
            return items[a:b]

        if is_search:
            page_items = generate_page_items(self.search_result)
        else:
            page_items = generate_page_items(self.items)

        if project_info is None:
            return page_items

        cache_list = page_items[:]
        for module in cache_list:
            module.is_download = False
            if isinstance(module, (Plugin, Adapter, Driver)):
                for item in getattr(
                    project_info, module.__class__.__name__.lower() + "s"
                ):
                    if module.module_name == item.module_name:
                        module.is_download = True
                        break

        return cache_list

    def search_item(self, project_meta: NoneBotProjectMeta, *, content: str) -> None:
        filters_pattern = r"(is:[^ ]+(?:\s+is:[^ ]+)*)"
        filter_pattern = r"is:([^ ]+)"

        result: List[_T] = list()

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

        filters_match = re.search(filters_pattern, content)
        if filters_match is None:
            custom_filter()
        else:
            filters = filters_match.group(1)
            content = content.replace(filters, str(), 1).strip()

            custom_filter()

            filters_match = re.findall(filter_pattern, filters)
            if filters_match:
                cache_list = result[:]

                if "downloaded" in filters_match:
                    item = safe_list_get(self.items, 0, str())
                    if isinstance(item, Plugin):
                        result = project_meta.plugins  # type: ignore
                    elif isinstance(item, Adapter):
                        result = project_meta.adapters  # type: ignore
                    elif isinstance(item, Driver):
                        result = project_meta.drivers  # type: ignore

                    if len(filters_match) == 1:
                        self.search_result = result
                        return

                for i in cache_list:
                    for f in filters_match:
                        if f == "official" and not i.is_official:
                            remove_item(i)
                        if f == "valid" and isinstance(i, Plugin) and not i.valid:
                            remove_item(i)
                        if f == "new" and isinstance(i, Plugin):
                            latest_time = (
                                datetime.now(timezone(timedelta(hours=8)))
                                - timedelta(weeks=1)
                            ).timestamp()
                            update_time = parser.parse(i.time).timestamp()
                            if update_time < latest_time:
                                remove_item(i)

        self.search_result = result


plugin_store_manager = ModuleStoreManager[Plugin](module_type="plugin")
adapter_store_manager = ModuleStoreManager[Adapter](module_type="adapter")
driver_store_manager = ModuleStoreManager[Driver](module_type="driver")
