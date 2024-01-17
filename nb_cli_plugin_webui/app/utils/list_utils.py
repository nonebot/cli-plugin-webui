from typing import Any, List


def safe_list_get(_list: List[Any], _index: int, default: Any) -> Any:
    try:
        return _list[_index]
    except IndexError:
        return default


def safe_list_remove(_list: List[Any], _item: Any) -> None:
    try:
        _list.remove(_item)
    except ValueError:
        pass
