from pathlib import Path
from typing import Any, Dict, List

from nb_cli.config import ConfigManager
from dotenv import set_key, dotenv_values
from pydantic import BaseModel, ValidationError
from nb_cli.exceptions import ProjectNotFoundError
from nb_cli.config import SimpleInfo as CliSimpleInfo

from nb_cli_plugin_webui.app.utils.storage import get_data_file
from nb_cli_plugin_webui.app.schemas import Plugin, ModuleInfo, NoneBotProjectMeta

from .store import plugin_store_manager
from .plugin import get_nonebot_plugin_list, get_nonebot_plugin_config_detail

PROJECTS_DATA_FILE_NAME = "projects.json"
PROJECTS_DATA_PATH = get_data_file(PROJECTS_DATA_FILE_NAME)


class NoneBotProjectList(BaseModel):
    projects: Dict[str, NoneBotProjectMeta]


class NoneBotProjectManager:
    meta_modifiable_keys = {
        "project_name",
        "mirror_url",
        "plugin_dirs",
        "use_run_script",
        "run_script_name",
    }

    def __init__(self, *, project_id: str) -> None:
        self.project_id = project_id

        try:
            self.read()
        except Exception:
            self.config_manager = ConfigManager(use_venv=True)

    @classmethod
    def _load(cls) -> NoneBotProjectList:
        try:
            return NoneBotProjectList.parse_file(PROJECTS_DATA_PATH, encoding="utf-8")
        except FileNotFoundError as err:
            raise err
        except ValidationError as err:
            raise err

    @classmethod
    def get_projects(cls) -> Dict[str, NoneBotProjectMeta]:
        return cls._load().projects

    def store(self, data: NoneBotProjectMeta) -> None:
        if not PROJECTS_DATA_PATH.exists():
            file = NoneBotProjectList(projects={self.project_id: data})
        else:
            file = self._load()
            file.projects[self.project_id] = data

        PROJECTS_DATA_PATH.write_text(file.json(), encoding="utf-8")

    def read(self) -> NoneBotProjectMeta:
        data = self._load()
        info = data.projects.get(self.project_id)
        if info is None:
            raise ProjectNotFoundError
        self.config_manager = ConfigManager(
            working_dir=Path(info.project_dir), use_venv=True
        )

        return info

    async def add_project(
        self,
        *,
        project_name: str,
        project_dir: Path,
        mirror_url: str,
        adapters: List[ModuleInfo] = list(),
        drivers: List[ModuleInfo] = list(),
        plugins: List[Plugin] = list(),
        plugin_dirs: List[str] = list(),
        builtin_plugins: List[str] = list(),
    ) -> None:
        self.store(
            NoneBotProjectMeta(
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
        )
        await self.update_plugin_config_schema()

    def remove_project(self) -> None:
        data = self._load()
        data.projects.pop(self.project_id)
        PROJECTS_DATA_PATH.write_text(data.json(), encoding="utf-8")

    def modify_meta(self, k: str, v: Any) -> None:
        data = self.read()
        if k in self.meta_modifiable_keys:
            setattr(data, k, v)
            self.store(data)

    def add_adapter(self, adapter: ModuleInfo) -> None:
        self.config_manager.add_adapter(
            CliSimpleInfo(name=adapter.name, module_name=adapter.module_name)
        )
        data = self.read()
        data.adapters.append(adapter)
        self.store(data)

    def remove_adapter(self, adapter: ModuleInfo) -> None:
        self.config_manager.remove_adapter(
            CliSimpleInfo(name=adapter.name, module_name=adapter.module_name)
        )
        data = self.read()
        for adapter in data.adapters:
            if adapter.module_name == adapter.module_name:
                data.adapters.remove(adapter)
                break
        self.store(data)

    async def update_plugin_config_schema(self) -> None:
        plugin_list = await get_nonebot_plugin_list(self.config_manager.python_path)
        for plugin in plugin_list:
            plugin_store_manager.search_item(self.read(), content=plugin)
            search_result = plugin_store_manager.get_item(is_search=True)
            if not search_result:
                break
            plugin_detail = None
            for i in search_result:
                if i.module_name == plugin:
                    plugin_detail = i
                    break

            if plugin_detail is None:
                break

            config_detail = await get_nonebot_plugin_config_detail(
                plugin, self.config_manager.python_path
            )
            raw_plugin_info = plugin_detail.dict()
            raw_plugin_info["config_detail"] = config_detail
            new_plugin_info = Plugin.parse_obj(raw_plugin_info)

            data = self.read()
            installed_plugin = [i.module_name for i in data.plugins]
            if plugin_detail.module_name not in installed_plugin:
                data.plugins.append(new_plugin_info)
            else:
                for plugin in data.plugins:
                    if plugin.module_name == plugin_detail.module_name:
                        plugin.config_detail = config_detail
                        break
            self.store(data)

    async def add_plugin(self, plugin: Plugin) -> None:
        self.config_manager.add_plugin(plugin.module_name)

        await self.update_plugin_config_schema()

    def remove_plugin(self, plugin: Plugin) -> None:
        self.config_manager.remove_plugin(plugin.module_name)

        data = self.read()
        cache_list = data.plugins[:]
        for i in cache_list:
            if i.module_name == plugin.module_name:
                data.plugins.remove(i)
        self.store(data)

    def add_builtin_plugin(self, plugin: str) -> None:
        data = self.read()
        data.builtin_plugins.append(plugin)
        self.store(data)

    def remove_builtin_plugin(self, plugin: str) -> None:
        self.config_manager.remove_builtin_plugin(plugin)

        data = self.read()
        data.builtin_plugins.remove(plugin)
        self.store(data)

    def add_driver(self, env: str, driver: ModuleInfo) -> None:
        data = self.read()

        env_path = Path(data.project_dir) / env
        env_data = dotenv_values(env_path)
        raw_drivers = env_data.get("DRIVER")
        if not raw_drivers:
            set_key(env_path, "DRIVER", driver.module_name)
        else:
            if driver.module_name not in raw_drivers:
                drivers = raw_drivers + f"+{driver.module_name}"
                set_key(env_path, "DRIVER", drivers)

        data.drivers.append(driver)
        self.store(data)

    def remove_driver(self, env: str, driver: ModuleInfo) -> None:
        data = self.read()

        env_path = Path(data.project_dir) / env
        env_data = dotenv_values(env_path)
        raw_drivers = env_data.get("DRIVER")
        if raw_drivers is None:
            set_key(env_path, "DRIVER", str())
        else:
            raw_drivers = raw_drivers.split("+")
            cache_list = raw_drivers[:]
            for old_driver in cache_list:
                if driver.module_name == old_driver:
                    raw_drivers.remove(driver.module_name)
            divers = "+".join(raw_drivers)
            set_key(env_path, "DRIVER", divers)

        for i in data.drivers:
            if i.module_name == driver.module_name:
                data.drivers.remove(i)
                break
        self.store(data)

    def write_to_env(self, env: str, k: str, v: Any) -> None:
        data = self.read()
        env_path = Path(data.project_dir) / env
        if not env_path.is_file():
            env_path.write_text(str(), encoding="utf-8")
        set_key(env_path, k, v)
