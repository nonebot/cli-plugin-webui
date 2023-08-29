import os
import asyncio
import threading
import subprocess
from pathlib import Path
from typing import Dict, Union, Optional, AsyncIterator

import psutil
from nb_cli.consts import WINDOWS
from nb_cli.handlers.process import terminate_process

from nb_cli_plugin_webui.utils import decode_parse
from nb_cli_plugin_webui.core.log import logger as log
from nb_cli_plugin_webui.exceptions import ProcessAlreadyRunning
from nb_cli_plugin_webui.models.domain.process import ProcessLog
from nb_cli_plugin_webui.models.schemas.process import ProcessInfo, ProcessPerformance
from nb_cli_plugin_webui.api.dependencies.process.log import (
    LoggerStorage as BaseLoggerStorage,
)


class LoggerStorage(BaseLoggerStorage[ProcessLog]):
    pass


class CustomProcessor:
    process: Optional[asyncio.subprocess.Process] = None
    process_is_running: bool = False
    process_thread: Optional[threading.Thread] = None

    def __init__(
        self,
        *args: Union[str, bytes, "os.PathLike[str]", "os.PathLike[bytes]"],
        cwd: Path,
        env: Optional[Dict[str, str]] = None,
        log_rotation_time: float = float(),
    ) -> None:
        self.args = args
        self.cwd = cwd
        self.env = env
        self.process_event = asyncio.Event()
        self.logs = LoggerStorage(log_rotation_time)

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
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if WINDOWS else 0,
        )
        assert self.process.stdin and self.process.stdout

        async def read_output():
            async for output in self.process.stdout:  # type: ignore
                output = decode_parse(output)
                if not output:
                    continue

                log_model = ProcessLog(message=output)
                await self.logs.add_log(log_model)

        if self.process.stdout:
            self.output_task = asyncio.create_task(read_output())

        async def error_exit():
            if self.process:
                await self.process.wait()
                await asyncio.sleep(5)
                await self.stop()

        self.error_task = asyncio.create_task(error_exit())

    def get_status(self):
        if not self.process or self.process.returncode is not None:
            return ProcessInfo(
                status_code=self.process.returncode if self.process else None,
                total_log=self.logs.get_count(),
                is_running=self.process_is_running,
                performance=None,
            )

        with (ps := psutil.Process(self.process.pid)).oneshot():
            cpu = ps.cpu_percent()
            mem = ps.memory_percent()

        return ProcessInfo(
            status_code=self.process.returncode,
            total_log=self.logs.get_count(),
            is_running=self.process_is_running,
            performance=ProcessPerformance(cpu=cpu, mem=mem),
        )

    def get_log_record(self) -> LoggerStorage:
        return self.logs

    async def start(self) -> None:
        if self.process_is_running:
            raise ProcessAlreadyRunning

        async for pid in self._find_duplicate_process():
            log.warning(f"Possible process {pid=} found, terminated.")

        self.process_is_running = True
        await self._process_executer()

    async def stop(self):
        self.process_is_running = False
        if self.process:
            pid = self.process.pid
            await terminate_process(self.process)
            log.info(f"Process {pid=} terminated.")

        if self.output_task:
            self.output_task.cancel()

        if self.error_task:
            self.error_task.cancel()

        log_model = ProcessLog(message="Process finished.")
        await self.logs.add_log(log_model)

    async def write_stdin(self, data: bytes) -> int:
        assert self.process and self.process.stdin
        self.process.stdin.write(data)
        await self.process.stdin.drain()
        return len(data)
