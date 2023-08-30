import asyncio
from typing import Set, Dict, List, Generic, TypeVar, Callable, Awaitable

from pydantic import BaseModel

from nb_cli_plugin_webui.exceptions import LoggerStorageAlreadyExist

_T = TypeVar("_T")
LogListener = Callable[[_T], Awaitable[None]]
DEFAULT_ROTATION_TIME: float = 5 * 60


class LoggerStorage(Generic[_T]):
    def __init__(self, rotation_time: float = DEFAULT_ROTATION_TIME) -> None:
        self.rotation_time = rotation_time
        self.logs: Dict[int, _T] = dict()
        self.listeners: Set[LogListener[_T]] = set()

    async def add_log(self, log: _T) -> int:
        log_seq = len(self.logs) + 1
        self.logs[log_seq] = log
        await self._notify_listeners(log)
        asyncio.get_running_loop().call_later(
            self.rotation_time, self.remove_log, log_seq
        )
        return log_seq

    def get_logs(
        self, reverse: bool = False, limit: int = 0, is_dict: bool = False
    ) -> List[_T]:
        if is_dict and isinstance(self.logs.get(0), BaseModel):
            logs = [
                # Stupid linter
                self.logs[log_seq].dict()  # type: ignore
                for log_seq in sorted(self.logs, reverse=reverse)
            ]
        else:
            logs = [
                self.logs[log_seq] for log_seq in sorted(self.logs, reverse=reverse)
            ]

        return logs[-limit:] if limit else logs

    def get_count(self) -> int:
        return len(self.logs)

    def register_listener(self, listener: LogListener[_T]) -> None:
        self.listeners.add(listener)

    def unregister_listener(self, listener: LogListener[_T]) -> None:
        self.listeners.remove(listener)

    async def _notify_listeners(self, log: _T) -> None:
        await asyncio.gather(
            *[listener(log) for listener in self.listeners], return_exceptions=True
        )

    def remove_log(self, seq: int) -> None:
        try:
            self.logs.pop(seq)
        except KeyError:
            pass
        return


class LoggerStorageFather(Generic[_T]):
    storages: Dict[str, LoggerStorage[_T]] = dict()

    get_storage = storages.get

    @classmethod
    def add_storage(cls, storage: LoggerStorage, key: str) -> None:
        if key in cls.storages:
            raise LoggerStorageAlreadyExist
        cls.storages[key] = storage

    @classmethod
    def remove_storage(cls, key: str) -> None:
        cls.storages.pop(key)
        return
