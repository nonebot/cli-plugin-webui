from typing import Any, List


def safe_list_get(_list: List[Any], _index: int, default: Any) -> Any:
    try:
        return _list[_index]
    except IndexError:
        return default
