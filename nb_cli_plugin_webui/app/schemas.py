from typing import Generic, TypeVar

from pydantic import BaseModel

_T = TypeVar("_T")


class GenericResponse(BaseModel, Generic[_T]):
    detail: _T
