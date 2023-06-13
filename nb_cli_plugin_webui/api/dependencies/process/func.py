import asyncio
from functools import partial
from typing import Dict, TypeVar, Callable, Awaitable

from nb_cli_plugin_webui.exceptions import FunctionAlreadyExist

_T = TypeVar("_T")
Func = Callable[[_T], Awaitable[None]]
DEFAULT_ROTATION_TIME: float = 60


class FuncStorage:
    functions: Dict[str, Func] = dict()

    get_func = functions.get

    @classmethod
    def add_func(
        cls, func: Func[_T], *args, key: str, rotate_time: float = DEFAULT_ROTATION_TIME
    ) -> None:
        if key in cls.functions:
            raise FunctionAlreadyExist
        cls.functions[key] = partial(func, *args)
        asyncio.get_running_loop().call_later(rotate_time, cls.remove_func, key)

    @classmethod
    def remove_func(cls, key: str) -> None:
        cls.functions.pop(key)
        return
