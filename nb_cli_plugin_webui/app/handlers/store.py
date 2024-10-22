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
from nb_cli_plugin_webui.app.models.types import ModuleType
from nb_cli_plugin_webui.app.models.store import Plugin, SearchTag
from nb_cli_plugin_webui.app.models.base import Driver, Adapter, NoneBotProjectMeta
from nb_cli_plugin_webui.app.utils.list_utils import safe_list_get, safe_list_remove

_T = TypeVar("_T", Plugin, Adapter, Driver)
VISIBLE_ITEMS = Config.extension_store_visible_items

if TYPE_CHECKING:

    @overload
    async def load_module_data(
        module_type: Literal[ModuleType.PLUGIN],
    ) -> List[Plugin]:
        ...

    @overload
    async def load_module_data(
        module_type: Literal[ModuleType.ADAPTER],
    ) -> List[Adapter]:
        ...

    @overload
    async def load_module_data(
        module_type: Literal[ModuleType.DRIVER],
    ) -> List[Driver]:
        ...

    async def load_module_data(
        module_type: ModuleType,
    ) -> Union[List[Plugin], List[Adapter], List[Driver]]:
        ...

else:

    @cache(ttl="5m")
    async def load_module_data(
        module_type: ModuleType,
    ) -> Union[List[Plugin], List[Adapter], List[Driver]]:
        if module_type == ModuleType.PLUGIN:
            module_class = Plugin
        elif module_type == ModuleType.ADAPTER:
            module_class = Adapter
        elif module_type == ModuleType.DRIVER:
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
        module_type: ModuleType,
        visible_items: int = VISIBLE_ITEMS,
    ) -> None:
        self.module_type = module_type
        self.visible_items = visible_items

        self.items: List[_T] = list()
        self.page = 1
        self.search_result: List[_T] = list()

    async def load_item(self) -> None:
        self.items = await load_module_data(self.module_type) or list()  # type: ignore

    def get_item(self, *, is_search: bool = False) -> List[_T]:
        if is_search:
            return self.search_result
        else:
            return self.items

    def get_max_page(self, *, is_search: bool = False) -> int:
        return math.ceil(
            len(self.search_result if is_search else self.items) / self.visible_items
        )

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
        elif self.page < 1:
            self.page = 1

        def generate_page_items(items: List[_T]) -> List[_T]:
            a = (self.page - 1) * self.visible_items
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

    def search_item(
        self,
        project_meta: NoneBotProjectMeta,
        *,
        content: str,
        tags: List[SearchTag] = list(),
    ):
        result: List[_T] = list()

        for item in self.items:
            if content in item.module_name:
                result.append(item)
            elif content in item.name:
                result.append(item)
            elif content in item.desc:
                result.append(item)
            elif content in item.author:
                result.append(item)
            elif item.project_link and content in item.project_link:
                result.append(item)

        data = result[:]
        # 部分需要整顿成例如 downloaded:yes / no
        for tag in tags:
            if tag.label == "official":
                for item in data:
                    if not item.is_official:
                        safe_list_remove(result, item)
            elif tag.label == "valid":
                for item in data:
                    if isinstance(item, Plugin) and not item.valid:
                        safe_list_remove(result, item)
            elif tag.label == "latest":
                if tag.text == "week":
                    for item in data:
                        if isinstance(item, Plugin):
                            latest_time = (
                                datetime.now(timezone(timedelta(hours=8)))
                                - timedelta(weeks=1)
                            ).timestamp()
                            update_time = parser.parse(item.time).timestamp()
                            if update_time < latest_time:
                                safe_list_remove(result, item)
                elif tag.text == "month":
                    for item in data:
                        if isinstance(item, Plugin):
                            latest_time = (
                                datetime.now(timezone(timedelta(hours=8)))
                                - timedelta(weeks=4)
                            ).timestamp()
                            update_time = parser.parse(item.time).timestamp()
                            if update_time < latest_time:
                                safe_list_remove(result, item)
            elif tag.label == "downloaded":
                item = safe_list_get(self.items, 0, str())
                if isinstance(item, Plugin):
                    for item in data:
                        if item.module_name not in [
                            plugin.module_name for plugin in project_meta.plugins
                        ]:
                            safe_list_remove(result, item)
                elif isinstance(item, Adapter):
                    for item in data:
                        if item.module_name not in [
                            adapter.module_name for adapter in project_meta.adapters
                        ]:
                            safe_list_remove(result, item)
                elif isinstance(item, Driver):
                    for item in data:
                        if item.module_name not in [
                            driver.module_name for driver in project_meta.drivers
                        ]:
                            safe_list_remove(result, item)
            elif tag.label == "author":
                for item in data:
                    if tag.text not in item.author:
                        safe_list_remove(result, item)
            elif tag.label == "tag":
                for item in data:
                    if item.tags:
                        for t in item.tags:
                            if tag.text not in t.label:
                                safe_list_remove(result, item)
                    else:
                        safe_list_remove(result, item)

        seen_models = list()
        unique_base_models = list()

        for model in result:
            if model.module_name not in seen_models:
                seen_models.append(model.module_name)
                unique_base_models.append(model)

        self.search_result = unique_base_models


plugin_store_manager = ModuleStoreManager[Plugin](module_type=ModuleType.PLUGIN)
adapter_store_manager = ModuleStoreManager[Adapter](module_type=ModuleType.ADAPTER)
driver_store_manager = ModuleStoreManager[Driver](module_type=ModuleType.DRIVER)
