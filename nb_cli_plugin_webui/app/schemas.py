from typing import Generic, TypeVar

from pydantic.generics import GenericModel

_T = TypeVar("_T")


class GenericResponse(GenericModel, Generic[_T]):
    detail: _T
