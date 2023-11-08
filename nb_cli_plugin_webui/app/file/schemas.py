from typing import List

from pydantic import BaseModel

from nb_cli_plugin_webui.app.schemas import GenericResponse


class SimpleModel(BaseModel):
    name: str
    is_dir: bool
    path: str


class FileInfo(SimpleModel):
    modified_time: str
    absolute_path: str


class FileResponse(GenericResponse[List[FileInfo]]):
    pass
