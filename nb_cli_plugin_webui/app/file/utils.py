from typing import List
from pathlib import Path

from .schemas import FileInfo


def list_file(path: Path, path_relative: Path = Path()) -> List[FileInfo]:
    data = list()
    for f in path.iterdir():
        if f.name == ".DS_Store":
            continue
        _path = (path / f.name).relative_to(path_relative)
        absolute_path = (path / f.name).resolve()
        data.append(
            FileInfo(
                name=f.name,
                is_dir=f.is_dir(),
                modified_time=str(f.stat().st_mtime),
                path=str(_path).replace("\\", "/"),
                absolute_path=str(absolute_path).replace("\\", "/"),
            )
        )
    return data
