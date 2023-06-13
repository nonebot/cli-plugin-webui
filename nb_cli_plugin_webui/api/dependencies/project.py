from pathlib import Path
from typing import Dict, List, Optional

from pydantic import PathNotAFileError
from nb_cli.config import SimpleInfo, ConfigManager

from nb_cli_plugin_webui import PLUGIN_NAME
from nb_cli_plugin_webui.utils.localstore import get_data_file
from nb_cli_plugin_webui.models.schemas.project import (
    NonebotProjectList,
    NonebotProjectMeta,
)
from nb_cli_plugin_webui.exceptions import (
    NonebotProjectIsNotExist,
    NonebotProjectFileIsNotExist,
)

PROJECTS_PATH = get_data_file(PLUGIN_NAME, "webui-nonebot-projects.json")


class NonebotProjectManager:
    def __init__(
        self,
        *,
        project_id: str,
    ) -> None:
        self.project_id = project_id

        try:
            self.read()
        except Exception:
            self.config_manager = ConfigManager(use_venv=True)

    @staticmethod
    def _load() -> NonebotProjectList:
        try:
            return NonebotProjectList.parse_file(PROJECTS_PATH)
        except PathNotAFileError:
            raise NonebotProjectFileIsNotExist
        except Exception as err:
            raise err

    @classmethod
    def get_projects(cls) -> Dict[str, Optional[NonebotProjectMeta]]:
        return cls._load().projects

    def add(
        self,
        *,
        project_name: str,
        project_dir: Path,
        mirror_url: str,
        adapters: List[SimpleInfo] = list(),
        drivers: List[SimpleInfo] = list(),
        plugins: List[str] = list(),
        plugin_dirs: List[str] = list(),
        builtin_plugins: List[str] = list(),
    ) -> None:
        meta = NonebotProjectMeta(
            project_id=self.project_id,
            project_name=project_name,
            project_dir=str(project_dir.absolute()),
            mirror_url=mirror_url,
            adapters=adapters,
            drivers=drivers,
            plugins=plugins,
            plugin_dirs=plugin_dirs,
            builtin_plugins=builtin_plugins,
        )
        self.store(meta)

    def remove(self):
        data = self._load()
        data.projects.pop(self.project_id)
        PROJECTS_PATH.write_text(data.json(), encoding="utf-8")

    def read(self) -> NonebotProjectMeta:
        data = self._load()

        info = data.projects.get(self.project_id)
        if info is None:
            raise NonebotProjectIsNotExist
        self.config_manager = ConfigManager(
            working_dir=Path(info.project_dir), use_venv=True
        )
        return info

    def store(self, data: NonebotProjectMeta) -> None:
        if not PROJECTS_PATH.is_file():
            raw = NonebotProjectList(projects=dict())
            PROJECTS_PATH.write_text(raw.json(), encoding="utf-8")

        file = NonebotProjectList.parse_file(PROJECTS_PATH)
        file.projects[self.project_id] = data
        PROJECTS_PATH.write_text(file.json(), encoding="utf-8")

    def add_adapter(self, adapter: SimpleInfo) -> None:
        self.config_manager.add_adapter(adapter)

        data = self.read()
        data.adapters.append(adapter)
        self.store(data)

    def remove_adapter(self, adapter: SimpleInfo) -> None:
        self.config_manager.remove_adapter(adapter)

        data = self.read()
        data.adapters.remove(adapter)
        self.store(data)

    def add_plugin(self, plugin: str) -> None:
        self.config_manager.add_plugin(plugin)

        data = self.read()
        data.plugins.append(plugin)
        self.store(data)

    def remove_plugin(self, plugin: str) -> None:
        self.config_manager.remove_plugin(plugin)

        data = self.read()
        data.plugins.remove(plugin)
        self.store(data)

    def add_builtin_plugin(self, plugin: str) -> None:
        self.config_manager.add_builtin_plugin(plugin)

        data = self.read()
        data.builtin_plugins.append(plugin)
        self.store(data)

    def remove_builtin_plugin(self, plugin: str) -> None:
        self.config_manager.remove_builtin_plugin(plugin)

        data = self.read()
        data.builtin_plugins.remove(plugin)
        self.store(data)
