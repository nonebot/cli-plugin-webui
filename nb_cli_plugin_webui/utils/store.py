from pathlib import Path
from typing import Callable
from typing_extensions import ParamSpec

from nb_cli.handlers.data import CONFIG_DIR, DATA_DIR, CACHE_DIR

P = ParamSpec("P")

APP_NAME = "nb-cli-plugin-webui"
BASE_CACHE_DIR = (CACHE_DIR / APP_NAME).resolve()
BASE_DATA_DIR = (DATA_DIR / APP_NAME).resolve()
BASE_CONFIG_DIR = (CONFIG_DIR / APP_NAME).resolve()


def _ensure_dir(path: Path) -> None:
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    elif not path.is_dir():
        raise RuntimeError(f"{path} is not a directory")


def _auto_create_dir(func: Callable[P, Path]) -> Callable[P, Path]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Path:
        path = func(*args, **kwargs)
        _ensure_dir(path)
        return path

    return wrapper


@_auto_create_dir
def get_cache_dir() -> Path:
    return BASE_CACHE_DIR


def get_cache_file(filename: str) -> Path:
    return get_cache_dir() / filename


@_auto_create_dir
def get_data_dir() -> Path:
    return BASE_DATA_DIR


def get_data_file(filename: str) -> Path:
    return get_data_dir() / filename


@_auto_create_dir
def get_config_dir() -> Path:
    return BASE_CONFIG_DIR


def get_config_file(filename: str) -> Path:
    return get_config_dir() / filename
