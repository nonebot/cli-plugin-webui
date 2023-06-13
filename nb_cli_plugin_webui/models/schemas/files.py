from typing import List

from pydantic import BaseModel


class FileMeta(BaseModel):
    name: str
    is_dir: int
    path: str


class FileDetails(FileMeta):
    modified_time: str
    absolute_path: str


class FilesInResponse(BaseModel):
    files: List[FileDetails]
