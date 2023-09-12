from typing import List
from pathlib import Path

from nb_cli_plugin_webui.core.configs.config import config
from nb_cli_plugin_webui.models.schemas.files import FileDetails

_conf = config.read()
BASE_DIR = Path(_conf.base_dir)


def get_files(path: Path, path_relative: Path = Path()) -> List[FileDetails]:
    data = list()
    for file in path.iterdir():
        if file.name == ".DS_Store":
            continue
        _path = (path / file.name).relative_to(path_relative)
        absolute_path = (path / file.name).resolve()
        data.append(
            FileDetails(
                name=file.name,
                is_dir=1 if file.is_dir() else 0,
                path=str(_path).replace("\\", "/"),
                modified_time=str(file.stat().st_mtime),
                absolute_path=str(absolute_path).replace("\\", "/"),
            )
        )
    return data
