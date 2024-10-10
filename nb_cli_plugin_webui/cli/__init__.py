import os
import webbrowser
from typing import List, cast

import click
from pydantic import ValidationError
from nb_cli.i18n import _ as nb_cli_i18n
from noneprompt import Choice, ListPrompt, ConfirmPrompt, CancelledError
from nb_cli.cli import CLI_DEFAULT_STYLE, ClickAliasedGroup, run_sync, run_async

from nb_cli_plugin_webui.i18n import _
from nb_cli_plugin_webui.app.application import STATIC_PATH
from nb_cli_plugin_webui.app.handlers.project import PROJECT_DATA_PATH
from nb_cli_plugin_webui.app.config import CONFIG_FILE_PATH, Config, generate_config

from .token import token
from .config import config
from .docker import docker


@click.group(
    cls=ClickAliasedGroup, invoke_without_command=True, help=_("Start up NB CLI UI.")
)
@click.pass_context
@run_async
async def webui(ctx: click.Context):
    if not STATIC_PATH.exists():
        click.secho(
            _("WebUI dist directory not found, please reinstall to fix."), fg="red"
        )
        return

    if not CONFIG_FILE_PATH.exists():
        if "WEBUI_BUILD" in os.environ:
            click.secho(
                _("Config not found in docker, run `nb ui docker` to fix."),
                fg="yellow",
            )
            return

        if not Config.check_necessary_config():
            await generate_config()
            return
    else:
        try:
            Config.load(CONFIG_FILE_PATH)
        except ValidationError:
            click.secho(_("Config file is broken, run `nb ui clear` to fix."), fg="red")
            return

    if ctx.invoked_subcommand is not None:
        return

    command = cast(ClickAliasedGroup, ctx.command)

    choices: List[Choice[click.Command]] = list()
    for sub_cmd_name in await run_sync(command.list_commands)(ctx):
        if sub_cmd := await run_sync(command.get_command)(ctx, sub_cmd_name):
            choices.append(
                Choice(
                    sub_cmd.help
                    or nb_cli_i18n("Run subcommand {sub_cmd.name!r}").format(
                        sub_cmd=sub_cmd
                    ),
                    sub_cmd,
                )
            )

    try:
        result = await ListPrompt(
            nb_cli_i18n("What do you want to do?"), choices=choices
        ).prompt_async(style=CLI_DEFAULT_STYLE)
    except CancelledError:
        ctx.exit()

    sub_cmd = result.data
    await run_sync(ctx.invoke)(sub_cmd)


@webui.command(help=_("Run WebUI."))
@click.option(
    "-h",
    "--host",
    type=str,
    show_default=True,
    help=_("The host required to access NB CLI UI."),
    default=None,
)
@click.option(
    "-p",
    "--port",
    type=int,
    show_default=True,
    help=_("The port required to access NB CLI UI."),
    default=None,
)
@run_async
async def run(host: str, port: int):
    from nb_cli_plugin_webui import server

    if not host:
        host = Config.host
    if not port:
        port = int(Config.port)
    else:
        if port < 1024 or port > 49151:
            click.secho(
                _("Port must be between 1024 and 49151. (Recommend: > 10000)"), fg="red"
            )
            return

    try:
        webbrowser.open(f"http://{host}:{port}/")
    except webbrowser.Error:
        pass
    await server.run_server(host, port)


@webui.command(help=_("Clear WebUI data."))
@run_async
async def clear():
    clear_file = await ListPrompt(
        _("Which data do you want to clear?"),
        choices=[
            Choice(CONFIG_FILE_PATH.name, CONFIG_FILE_PATH),
            Choice(PROJECT_DATA_PATH.name, PROJECT_DATA_PATH),
        ],
    ).prompt_async(style=CLI_DEFAULT_STYLE)

    if not await ConfirmPrompt(_("Are you sure to clear?")).prompt_async(
        style=CLI_DEFAULT_STYLE
    ):
        return

    if not clear_file.data.exists():
        click.secho(_("File not found."), fg="yellow")
        return

    try:
        os.remove(clear_file.data)
    except Exception as e:
        click.secho(str(e), fg="red")
        return

    click.secho(_("File cleared."), fg="green")


webui.add_command(config)
webui.add_command(docker)
webui.add_command(token)
