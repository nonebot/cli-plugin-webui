import asyncio
import traceback
from typing import Any, Dict, List, Tuple, Callable, Optional, get_type_hints

from .log import LogStorage
from .schemas import CustomLog


class ProcessFuncWithLog:
    def __init__(self, log: LogStorage) -> None:
        self.log = log
        self.queue: List[Tuple[Callable[..., Any], Tuple[Any, ...], Dict[str, Any]]] = (
            list()
        )

    async def _err_parse(
        self, err: Exception, additional_err_msg: Optional[str] = None
    ) -> None:
        tb = traceback.extract_tb(err.__traceback__)
        # 只保留项目代码的帧，过滤 asyncio/starlette 等内部帧
        project_frames = [f for f in tb if "nb_cli_plugin_webui" in f.filename]
        frames = project_frames if project_frames else tb[-3:]

        lines = ["Traceback (most recent call last):"]
        for frame in frames:
            lines.append(
                f'  File "{frame.filename}", line {frame.lineno}, in {frame.name}'
            )
            if frame.line:
                lines.append(f"    {frame.line}")
        lines.append(f"{type(err).__name__}: {err}")
        await self.log.add_log(CustomLog(message="\n".join(lines)))

        if additional_err_msg:
            await self.log.add_log(CustomLog(message=additional_err_msg))

        await self.log.add_log(CustomLog(message="❌ Failed!"))
        self.queue.clear()

    def add(
        self,
        func: Callable,
        *args,
        **kwargs,
    ) -> "ProcessFuncWithLog":
        self.queue.append((func, args, kwargs))
        return self

    async def _done(self, additional_err_msg: Optional[str]) -> None:
        for func, args, kwargs in self.queue:
            try:
                hints = get_type_hints(func)
                if hints.get("return") is bool:
                    if asyncio.iscoroutinefunction(func):
                        _ = await func(*args, **kwargs)
                    else:
                        _ = await asyncio.to_thread(func, *args, **kwargs)

                if asyncio.iscoroutinefunction(func):
                    await func(*args, **kwargs)
                else:
                    await asyncio.to_thread(func, *args, **kwargs)
            except Exception as err:
                await self._err_parse(err, additional_err_msg)
                break

    def done(self, *, additional_err_msg: Optional[str] = None) -> None:
        asyncio.create_task(self._done(additional_err_msg))
