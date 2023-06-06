from typing import List
from pathlib import Path

from nb_cli_plugin_webui.core.configs.config import config
from nb_cli_plugin_webui.models.schemas.files import FileInfo

_conf = config.read()
BASE_DIR = Path(_conf.base_dir)


def get_files(path: Path) -> List[FileInfo]:
    path = BASE_DIR / path
    data = list()
    for file in path.iterdir():
        data.append(
            FileInfo(
                name=file.name,
                modified_time=str(file.stat().st_mtime),
                is_dir=1 if file.is_dir() else 0,
                path=str(Path(path / file.name).relative_to(BASE_DIR).resolve()),
            )
        )
    return data
