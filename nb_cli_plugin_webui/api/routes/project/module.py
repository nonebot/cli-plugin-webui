import re
import asyncio
from typing import Any
from pathlib import Path

from nb_cli.handlers.pip import call_pip_uninstall
from fastapi import Body, APIRouter, HTTPException, status

from nb_cli_plugin_webui.utils import generate_complexity_string
from nb_cli_plugin_webui.exceptions import NonebotProjectIsNotExist
from nb_cli_plugin_webui.api.dependencies.pip import call_pip_install
from nb_cli_plugin_webui.models.domain.process import LogLevel, CustomLog
from nb_cli_plugin_webui.api.dependencies.project import (
    NonebotProjectManager,
    check_toml,
)
from nb_cli_plugin_webui.api.dependencies.process.log import (
    LoggerStorage,
    LoggerStorageFather,
)
from nb_cli_plugin_webui.models.schemas.project import (
    Plugin,
    SimpleInfo,
    InstallModuleResponse,
    CheckProjectTomlResponse,
)

router = APIRouter()


@router.post("/install", response_model=InstallModuleResponse)
async def install_nonebot_project_module(
    project_id: str = Body(embed=True),
    env: str = Body(embed=True),
    module: Any = Body(embed=True),
) -> InstallModuleResponse:
    project = NonebotProjectManager(project_id)
    try:
        project.read()
    except NonebotProjectIsNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"实例 {project_id=} 不存在"
        )

    try:
        module = Plugin.parse_obj(module)
    except Exception:
        module = SimpleInfo.parse_obj(module)

    project_detail = project.read()
    log = LoggerStorage()
    log_key = generate_complexity_string(8)
    LoggerStorageFather.add_storage(log, log_key)

    async def process(module: SimpleInfo, log: LoggerStorage):
        async def _err_parse(err: Exception):
            log_model = CustomLog(level=LogLevel.ERROR, message=str(err))
            await log.add_log(log_model)

            log_model = CustomLog(message="❗ Failed...")
            await log.add_log(log_model)
            raise err

        await asyncio.sleep(1)

        log_model = CustomLog(message="Processing at 3s...")
        await log.add_log(log_model)

        await asyncio.sleep(3)

        log_model = CustomLog(message=f"Install module name: {module.module_name}")
        await log.add_log(log_model)

        try:
            proc, log = await call_pip_install(
                module.project_link,
                ["-i", project_detail.mirror_url],
                log_storage=log,
                python_path=project.config_manager.python_path,
            )
            await proc.wait()
        except Exception as err:
            await _err_parse(err)
            return

        if "~" not in module.module_name:
            pattern = r"nonebot-(.*?)-"
            _match = re.search(pattern, module.project_link)
            if _match is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="模块类型未找到"
                )
            module_type = _match.group(1)
        else:
            module_type = "driver"

        try:
            if module_type == "plugin" and isinstance(module, Plugin):
                await project.add_plugin(module)
            elif module_type == "adapter":
                project.add_adapter(module)
            elif module_type == "driver":
                project.add_driver(env, module)
        except Exception as err:
            await _err_parse(err)
            return

        log_model = CustomLog(message="✨ Done!")
        await log.add_log(log_model)

    asyncio.create_task(process(module, log))
    asyncio.get_running_loop().call_later(
        600, LoggerStorageFather.storages.pop, log_key
    )

    return InstallModuleResponse(log_key=log_key)


@router.post("/uninstall")
async def uninstall_nonebot_project_module(
    project_id: str = Body(embed=True),
    env: str = Body(embed=True),
    module: Any = Body(embed=True),
):
    project = NonebotProjectManager(project_id)
    try:
        project_detail = project.read()
    except NonebotProjectIsNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"实例 {project_id=} 不存在"
        )

    try:
        module = Plugin.parse_obj(module)
    except Exception:
        module = SimpleInfo.parse_obj(module)

    package = module.project_link
    if package.startswith("nonebot2[") and package.endswith("]"):
        package = package[9:-1]

    ob_adapter_prefix = "nonebot.adapters.onebot"
    if module.module_name.startswith(ob_adapter_prefix):
        ob_count = int()
        for adapter in project_detail.adapters:
            if adapter.module_name.startswith(ob_adapter_prefix):
                ob_count += 1

        if ob_count == 1:
            proc = await call_pip_uninstall(
                package,
                ["-y"],
                python_path=project.config_manager.python_path,
                stdout=asyncio.subprocess.PIPE,
            )
            await proc.wait()
    else:
        proc = await call_pip_uninstall(
            package,
            ["-y"],
            python_path=project.config_manager.python_path,
            stdout=asyncio.subprocess.PIPE,
        )
        await proc.wait()

    module_type = None
    pattern = r"nonebot-(.*?)-"
    _match = re.search(pattern, package)
    if _match:
        module_type = _match.group(1)

    pattern = r"~(.*?)"
    _match = re.search(pattern, module.module_name)
    if _match:
        module_type = "driver"

    if module_type is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="模块类型未找到")

    try:
        if module_type == "plugin" and isinstance(module, Plugin):
            project.remove_plugin(module)
        elif module_type == "adapter":
            project.remove_adapter(module)
        elif module_type == "driver":
            project.remove_driver(env, module)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"移除拓展信息失败: {err}"
        )

    return {"detail": "ok"}


@router.post("/check_toml", response_model=CheckProjectTomlResponse)
async def scan_nonebot(
    project_dir: str = Body(embed=True),
) -> CheckProjectTomlResponse:
    path = Path(project_dir)
    try:
        check = check_toml(path)
    except FileNotFoundError:
        return CheckProjectTomlResponse(
            is_pass=False, level="error", msg="未找到文件 'pyproject.toml'"
        )
    except Exception as err:
        return CheckProjectTomlResponse(
            is_pass=False, level="error", msg=f"其它未知错误：{err}"
        )

    msg = str()
    if not check.project_name:
        msg += "未找到项目名称,"
    if not check.adapters:
        msg += "未找到适配器,"
    if not check.plugins:
        msg += "未找到插件,"
    if not check.plugin_dirs:
        msg += "未找到插件目录,"
    if not check.builtin_plugins:
        msg += "未找到内置插件,"

    if not msg:
        msg = "检查通过"
        return CheckProjectTomlResponse(
            is_pass=True, level="success", msg=msg, detail=check
        )
    else:
        return CheckProjectTomlResponse(
            is_pass=True, level="warning", msg=msg, detail=check
        )
