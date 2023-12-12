import os
from pathlib import Path
from subprocess import check_output
from importlib.metadata import version


def __get_git_revision(path: Path):
    git_path = path / ".git"
    if not git_path.exists():
        return None
    try:
        revision = check_output(["git", "rev-parse", "HEAD"], cwd=path, env=os.environ)
    except Exception:
        return None
    return revision.decode("utf-8").strip()


def get_revision():
    if "WEBUI_BUILD" in os.environ:
        return os.environ["WEBUI_BUILD"]
    package_dir = Path(__file__)
    if package_dir.exists():
        return __get_git_revision(package_dir.parent.parent.absolute())


def get_version():
    if __build__:
        return f"{__version__}.{__build__}"
    return __version__


__version__ = version("nb_cli_plugin_webui")
__build__ = get_revision()
