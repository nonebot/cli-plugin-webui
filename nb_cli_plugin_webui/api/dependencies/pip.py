import asyncio
from typing import IO, Any, List, Tuple, Union, Optional

from nb_cli.handlers.meta import requires_pip, get_default_python

from nb_cli_plugin_webui.api.dependencies.process.log import LoggerStorage
from nb_cli_plugin_webui.api.dependencies.process.impl import (
    run_asyncio_subprocess_with_logging,
)


@requires_pip
async def call_pip(
    pip_args: Optional[List[str]] = None,
    *,
    python_path: Optional[str] = None,
    stdin: Optional[Union[IO[Any], int]] = None,
    log_storage: LoggerStorage,
) -> Tuple[asyncio.subprocess.Process, LoggerStorage]:
    if pip_args is None:
        pip_args = list()
    if python_path is None:
        python_path = await get_default_python()

    return await run_asyncio_subprocess_with_logging(
        python_path, "-m", "pip", *pip_args, stdin=stdin, log_storage=log_storage
    )


@requires_pip
async def call_pip_install(
    package: Union[str, List[str]],
    pip_args: Optional[List[str]] = None,
    *,
    python_path: Optional[str] = None,
    stdin: Optional[Union[IO[Any], int]] = None,
    log_storage: LoggerStorage,
) -> Tuple[asyncio.subprocess.Process, LoggerStorage]:
    if isinstance(package, str):
        package = [package]
    if pip_args is None:
        pip_args = list()

    return await call_pip(
        ["install", *package, *pip_args],
        python_path=python_path,
        stdin=stdin,
        log_storage=log_storage,
    )
