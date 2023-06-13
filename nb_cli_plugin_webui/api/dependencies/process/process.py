import time
import asyncio
import threading
import subprocess
from pathlib import Path
from itertools import count
from typing import List, Optional, AsyncIterator

import psutil
from nb_cli.cli import run_sync

from nb_cli_plugin_webui.core.log import logger as log
from nb_cli_plugin_webui.exceptions import ProcessAlreadyRunning
from nb_cli_plugin_webui.models.domain.process import ProcessLog
from nb_cli_plugin_webui.api.dependencies.process.log import (
    LoggerStorage as BaseLoggerStorage,
)


class LoggerStorage(BaseLoggerStorage[ProcessLog]):
    pass


class CustomProcessor:
    process: Optional[subprocess.Popen] = None
    process_is_running: bool = False
    process_thread: Optional[threading.Thread] = None

    def __init__(
        self,
        command: List[str],
        cwd: Path,
        log_rotation_time: float = float(),
        kill_timeout: int = 10,
        stop_timeout: int = 10,
        max_retry: int = 3,
        retry_interval: int = 5,
        post_delay: float = 3,
    ) -> None:
        self.command = command
        self.cwd = cwd
        self.kill_timeout = kill_timeout
        self.stop_timeout = stop_timeout
        self.max_retry = max_retry
        self.retry_interval = retry_interval
        self.post_delay = post_delay
        self.retry_count = int()
        self.loop = asyncio.get_running_loop()
        self.logs = LoggerStorage(log_rotation_time)

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

    def _terminate_process(
        self, process: subprocess.Popen, timeout: float
    ) -> Optional[int]:
        process.terminate()
        try:
            return process.wait(timeout)
        except subprocess.TimeoutExpired:
            process.kill()

    def _process_executer(self) -> int:
        self.process = subprocess.Popen(
            self.command,
            cwd=self.cwd.absolute(),
            text=False,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        assert self.process.stdin and self.process.stdout

        for output in iter(self.process.stdout.readline, b""):
            output = output.strip().decode("utf-8", "replace")

            log_model = ProcessLog(message=output)
            asyncio.run_coroutine_threadsafe(
                self.logs.add_log(log_model), loop=self.loop
            )

        return self.process.returncode

    def _process_worker(self) -> None:
        for i in count():
            if not self.process_is_running:
                break
            if self.max_retry >= 0 and i >= self.max_retry:
                break

            code = None
            try:
                code = self._process_executer()
            except Exception:
                log.exception(
                    f"Thread {self.process_thread!r} raised unknown exception."
                )

            log.warning(
                f"Process for {self.command!r} exited with code {code}, retrying... "
                f"({i}/{self.max_retry})"
            )

            self.retry_count += 1
            time.sleep(self.retry_interval)

    async def start(self) -> None:
        if self.process_is_running:
            raise ProcessAlreadyRunning

        self.process_is_running = True
        self.process_thread = threading.Thread(target=self._process_worker, daemon=True)
        self.process_thread.start()

    @run_sync
    def stop(self) -> None:
        self.process_is_running = False
        if self.process is not None:
            self._terminate_process(self.process, self.post_delay)
        if self.process_thread and self.process_thread.is_alive():
            self.process_thread.join(self.stop_timeout)
            self.process_thread = None

    @run_sync
    def write_stdin(self, data: str) -> int:
        assert self.process and self.process.stdin
        wrote = self.process.stdin.write(data)
        self.process.stdin.flush()
        return wrote


class NonebotProcessor(CustomProcessor):
    ...
