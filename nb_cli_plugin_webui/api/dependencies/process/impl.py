import os
import asyncio
import subprocess
from pathlib import Path
from asyncio.streams import StreamReader
from typing import IO, Any, Tuple, Union, Optional

from nb_cli.consts import WINDOWS

from nb_cli_plugin_webui.models.domain.process import ProcessLog
from nb_cli_plugin_webui.api.dependencies.process.log import LoggerStorage


async def run_asyncio_subprocess_with_logging(
    *args: Union[str, bytes, "os.PathLike[str]", "os.PathLike[bytes]"],
    cwd: Optional[Path] = None,
    stdin: Optional[Union[IO[Any], int]] = None,
    log_storage: LoggerStorage = LoggerStorage(),
) -> Tuple[asyncio.subprocess.Process, LoggerStorage]:
    async def _read_stream(stream: Optional[StreamReader], log_storage: LoggerStorage):
        if stream:
            while True:
                line = await stream.readline()
                if line:
                    decode_line = line.decode("utf-8", "replace")
                    log_model = ProcessLog(message=decode_line)
                    await log_storage.add_log(log_model)
                else:
                    break

    process = await asyncio.create_subprocess_exec(
        *args,
        cwd=cwd,
        stdin=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if WINDOWS else 0,
    )

    asyncio.create_task(_read_stream(process.stdout, log_storage))
    asyncio.create_task(_read_stream(process.stderr, log_storage))

    return process, log_storage
