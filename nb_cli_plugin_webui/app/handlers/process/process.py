import os
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Union, Optional, AsyncIterator

import psutil
from nb_cli.consts import WINDOWS
from nb_cli.handlers.process import terminate_process

from nb_cli_plugin_webui.app.logging import logger as log
from nb_cli_plugin_webui.app.utils.string_utils import decode_parse

from .exceptions import ProcessAlreadyExists
from .log import LogStorage as BaseLogStorage
from .schemas import ProcessLog, ProcessInfo, ProcessPerformance


class LogStorage(BaseLogStorage[ProcessLog]):
    pass


class Processor:
    process: Optional[asyncio.subprocess.Process] = None
    process_is_running: bool = False

    def __init__(
        self,
        *args: Union[str, bytes, "os.PathLike[str]", "os.PathLike[bytes]"],
        cwd: Path,
        env: Optional[Dict[str, str]] = None,
        log_destroy_seconds: int,
    ) -> None:
        self.args = args
        self.cwd = cwd
        self.env = env
        self.log_storage = LogStorage(log_destroy_seconds)

        self.process_event = asyncio.Event()
        self.output_task = None
        self.error_task = None

    async def _find_duplicate_process(self) -> AsyncIterator[int]:
        for process in psutil.process_iter():
            try:
                with process.oneshot():
                    pid = process.pid
                    cwd = Path(process.cwd()).absolute()
            except psutil.Error:
                continue

            if not (cwd.is_dir()):
                continue
            if self.cwd.absolute() == cwd:
                process.terminate()
                yield pid

        return

    async def _process_executer(self) -> Optional[int]:
        self.process = await asyncio.create_subprocess_exec(
            *self.args,
            cwd=self.cwd,
            env=self.env,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            creationflags=(
                subprocess.CREATE_NEW_PROCESS_GROUP if WINDOWS else 0  # type: ignore
            ),
        )
        assert self.process.stdin and self.process.stdout

        async def read_output():
            async for output in self.process.stdout:  # type: ignore
                output = decode_parse(output)
                if not output:
                    continue

                log_model = ProcessLog(message=output)
                await self.log_storage.add_log(log_model)

        if self.process.stdout:
            self.output_task = asyncio.create_task(read_output())

        async def error_exit():
            if self.process:
                await self.process.wait()
                await asyncio.sleep(5)
                await self.stop()

        self.error_task = asyncio.create_task(error_exit())  # type: ignore

    def get_status(self) -> ProcessInfo:
        if not self.process or self.process.returncode is not None:
            return ProcessInfo(
                status_code=self.process.returncode if self.process else None,
                total_log=self.log_storage.get_count(),
                is_running=self.process_is_running,
                performance=None,
            )

        with (ps := psutil.Process(self.process.pid)).oneshot():
            cpu = ps.cpu_percent()
            mem = ps.memory_percent()

        return ProcessInfo(
            status_code=self.process.returncode,
            total_log=self.log_storage.get_count(),
            is_running=self.process_is_running,
            performance=ProcessPerformance(cpu=cpu, mem=mem),
        )

    async def start(self) -> None:
        if self.process_is_running:
            return

        async for pid in self._find_duplicate_process():
            log.warning(f"Possible process {pid=} found, terminated.")

        await self._process_executer()
        self.process_is_running = True

    async def stop(self):
        if self.process:
            pid = self.process.pid
            await terminate_process(self.process)
            self.process_is_running = False
            log.info(f"Process {pid=} terminated.")

        if self.output_task:
            self.output_task.cancel()

        if self.error_task:
            self.error_task.cancel()

        log_model = ProcessLog(message="Process finished.")
        await self.log_storage.add_log(log_model)

    async def write_stdin(self, data: bytes) -> int:
        assert self.process and self.process.stdin
        self.process.stdin.write(data)
        await self.process.stdin.drain()
        return len(data)


class ProcessManager:
    processes: Dict[str, Processor] = dict()

    get_process = processes.get

    @classmethod
    def add_process(cls, process: Processor, key: str) -> None:
        if key in cls.processes:
            raise ProcessAlreadyExists
        cls.processes[key] = process

    @classmethod
    def remove_process(cls, key: str) -> None:
        process = cls.processes.pop(key)
        process.log_storage.listeners.clear()
        return
