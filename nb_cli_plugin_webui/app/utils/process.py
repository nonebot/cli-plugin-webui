from pathlib import Path
from typing import Optional
from asyncio import subprocess

from nb_cli.handlers.process import create_process


async def run_python_script(
    python_path: str, script: str, cwd: Optional[Path] = None
) -> str:
    proc = await create_process(
        python_path,
        "-c",
        script,
        stdout=subprocess.PIPE,
        cwd=cwd,
    )
    stdout, _ = await proc.communicate()
    return stdout.decode().strip()
