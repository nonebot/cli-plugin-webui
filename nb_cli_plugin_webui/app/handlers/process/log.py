import asyncio
from typing import Set, Dict, List, Generic, TypeVar, Callable, Awaitable

from .exceptions import LogStorageAlreadyExists

_T = TypeVar("_T")

LogListener = Callable[[_T], Awaitable[None]]


class LogStorage(Generic[_T]):
    def __init__(self, destroy_seconds: int) -> None:
        self.destroy_seconds = destroy_seconds
        self.logs: Dict[int, _T] = dict()
        self.listeners: Set[LogListener[_T]] = set()

    async def add_log(self, log: _T) -> int:
        log_seq = len(self.logs) + 1
        self.logs[log_seq] = log
        await self._notify_listeners(log)
        asyncio.get_event_loop().call_later(
            self.destroy_seconds, self.remove_log, log_seq
        )
        return log_seq

    def get_logs(self, *, reverse: bool = False, count: int = 0) -> List[_T]:
        logs = [self.logs[log_seq] for log_seq in sorted(self.logs, reverse=reverse)]
        return logs[-count:] if count else logs

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


class LogStorageFather(Generic[_T]):
    storages: Dict[str, LogStorage[_T]] = dict()

    get_storage = storages.get

    @classmethod
    def add_storage(cls, storage: LogStorage, key: str) -> None:
        if key in cls.storages:
            raise LogStorageAlreadyExists
        cls.storages[key] = storage

    @classmethod
    def remove_storage(cls, key: str) -> None:
        cls.storages.pop(key)
        return
