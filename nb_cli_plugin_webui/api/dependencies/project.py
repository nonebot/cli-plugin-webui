from pathlib import Path
from typing import Any, Dict, List

import tomlkit
from pydantic import PathNotAFileError
from nb_cli.config import ConfigManager
from dotenv import set_key, dotenv_values
from nb_cli.config import SimpleInfo as CliSimpleInfo

from nb_cli_plugin_webui.utils.store import get_data_file
from nb_cli_plugin_webui.models.schemas.store import SimpleInfo
from nb_cli_plugin_webui.api.dependencies.store.manage import PLUGIN_MANAGER
from nb_cli_plugin_webui.exceptions import InvalidKeyException, NonebotProjectIsNotExist
from nb_cli_plugin_webui.api.dependencies.plugin import (
    get_plugin_list,
    get_plugin_config_detail,
)
from nb_cli_plugin_webui.models.schemas.project import (
    Plugin,
    NonebotProjectList,
    NonebotProjectMeta,
    CheckProjectTomlDetail,
)


class NonebotProjectManager:
    project_file_name = "webui-nonebot-projects.json"
    project_file_path = get_data_file(project_file_name)

    meta_modifiable_key = {
        "project_name",
        "mirror_url",
        "plugin_dirs",
        "use_run_script",
        "run_script_name",
    }

    def __init__(
        self,
        project_id: str,
    ) -> None:
        self.project_id = project_id

        try:
            self.read()
        except Exception:
            self.config_manager = ConfigManager(use_venv=True)

    @classmethod
    def _load(cls) -> NonebotProjectList:
        try:
            return NonebotProjectList.parse_file(cls.project_file_path)
        except PathNotAFileError:
            raise NonebotProjectIsNotExist
        except FileNotFoundError:
            raise NonebotProjectIsNotExist

    @classmethod
    def get_projects(cls) -> Dict[str, NonebotProjectMeta]:
        return cls._load().projects

    def add(
        self,
        *,
        project_name: str,
        project_dir: Path,
        mirror_url: str,
        adapters: List[SimpleInfo] = list(),
        drivers: List[SimpleInfo] = list(),
        plugins: List[Plugin] = list(),
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
        self.project_file_path.write_text(data.json(), encoding="utf-8")

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
        if not self.project_file_path.is_file():
            raw = NonebotProjectList(projects=dict())
            self.project_file_path.write_text(raw.json(), encoding="utf-8")

        file = NonebotProjectList.parse_file(self.project_file_path)
        file.projects[self.project_id] = data
        self.project_file_path.write_text(file.json(), encoding="utf-8")

    def modify_meta(self, k: str, v: Any) -> None:
        if k in self.meta_modifiable_key:
            data = self.read()
            setattr(data, k, v)
            self.store(data)
        else:
            raise InvalidKeyException

    def add_adapter(self, adapter: SimpleInfo) -> None:
        self.config_manager.add_adapter(
            CliSimpleInfo(name=adapter.name, module_name=adapter.module_name)
        )

        data = self.read()
        data.adapters.append(adapter)
        self.store(data)

    def remove_adapter(self, adapter: SimpleInfo) -> None:
        self.config_manager.remove_adapter(
            CliSimpleInfo(name=adapter.name, module_name=adapter.module_name)
        )

        data = self.read()
        for a in data.adapters:
            if a.module_name == adapter.module_name:
                data.adapters.remove(a)
                break
        self.store(data)

    async def update_plugin_config_schema(self) -> None:
        plugin_list = await get_plugin_list(self.config_manager.python_path)
        for plugin in plugin_list:
            PLUGIN_MANAGER.search_item(self.read(), plugin)
            search_result = PLUGIN_MANAGER.get_item(is_search=True)
            if not search_result:
                break
            plugin_detail = None
            for i in search_result:
                if i.module_name == plugin:
                    plugin_detail = i
                    break

            if plugin_detail is None:
                break

            config_detail = await get_plugin_config_detail(
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
                for i in data.plugins:
                    if i.project_link == plugin_detail.project_link:
                        data.plugins.remove(i)
                        data.plugins.append(new_plugin_info)
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
        self.config_manager.add_builtin_plugin(plugin)

        data = self.read()
        data.builtin_plugins.append(plugin)
        self.store(data)

    def remove_builtin_plugin(self, plugin: str) -> None:
        self.config_manager.remove_builtin_plugin(plugin)

        data = self.read()
        data.builtin_plugins.remove(plugin)
        self.store(data)

    def add_driver(self, env: str, driver: SimpleInfo) -> None:
        data = self.read()
        data.drivers.append(driver)
        self.store(data)

        env_path = Path(data.project_dir) / env
        env_data = dotenv_values(env_path)
        raw_drivers = env_data.get("DRIVER")
        if not raw_drivers:
            set_key(env_path, "DRIVER", driver.module_name)
        else:
            if driver.module_name not in raw_drivers:
                drivers = raw_drivers + f"+{driver.module_name}"
                set_key(env_path, "DRIVER", drivers)

    def remove_driver(self, env: str, driver: SimpleInfo) -> None:
        data = self.read()
        for d in data.drivers:
            if d.module_name == driver.module_name:
                data.drivers.remove(d)
                break
        self.store(data)

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
            drivers = "+".join(raw_drivers)
            set_key(env_path, "DRIVER", drivers)

    def write_to_env(self, env: str, k: str, v: Any) -> None:
        """写入 dotenv 文件，如目标文件不存在，则创建再写入

        Args:
            - env (str): 目标环境名称，留空则默认 `.env`
            - k (str): 目标 key
            - v (Any): 目标 key 对应的 value
        """

        data = self.read()

        env_path = Path(data.project_dir) / env
        if not env_path.is_file():
            with open(env_path, "w", encoding="utf-8") as w:
                w.write(str())

        env_data = dotenv_values(env_path)
        target = env_data.get(k)
        if target is None:
            set_key(env_path, k, v)
        else:
            set_key(env_path, k, v)


def check_toml(working_dir: Path) -> CheckProjectTomlDetail:
    path = working_dir / "pyproject.toml"
    if not path.is_file():
        raise FileNotFoundError
    data = tomlkit.loads(path.read_text(encoding="utf-8"))

    project_name = data.get("project", dict()).get("name", str())
    tool_detail = data.get("tool", dict())

    nonebot_info = tool_detail.get("nonebot", dict())
    adapters = nonebot_info.get("adapters", list())
    plugins = nonebot_info.get("plugins", list())
    plugin_dirs = nonebot_info.get("plugin_dirs", list())

    # TODO
    builtin_plugins = list()

    return CheckProjectTomlDetail(
        project_name=project_name,
        adapters=adapters,
        plugins=plugins,
        plugin_dirs=plugin_dirs,
        builtin_plugins=builtin_plugins,
    )
