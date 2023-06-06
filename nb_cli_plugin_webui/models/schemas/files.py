from typing import List

from pydantic import BaseModel


class FileInfo(BaseModel):
    name: str
    modified_time: str
    is_dir: int
    path: str


class FileListRequest(BaseModel):
    path: str


class FileOperateRequest(BaseModel):
    file_name: str
    is_dir: int
    path: str


class FilesInResponse(BaseModel):
    files: List[FileInfo]
