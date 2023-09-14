from asyncio import create_task, as_completed
from typing import TYPE_CHECKING, List, Union, Literal, overload

import httpx
from nb_cli import cache
from nb_cli.exceptions import ModuleLoadFailed

from nb_cli_plugin_webui.i18n import _
from nb_cli_plugin_webui.core.log import logger as log
from nb_cli_plugin_webui.models.schemas.store import Driver, Plugin, Adapter

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
        urls = [
            f"https://registry.nonebot.dev/{module_name}.json",
            f"https://cdn.jsdelivr.net/gh/nonebot/registry@results/{module_name}.json",
            f"https://cdn.staticaly.com/gh/nonebot/registry@results/{module_name}.json",
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
                log.error(f"获取 {module_name} 列表失败: {err}")

        raise ModuleLoadFailed(
            _("Failed to get {module_type} list.").format(module_type=module_type)
        )
