import shutil
from pathlib import Path
from typing import List, cast

import click
from nb_cli.i18n import _ as nb_cli_i18n
from noneprompt import Choice, ListPrompt, CancelledError
from nb_cli.cli import CLI_DEFAULT_STYLE, ClickAliasedGroup, run_sync, run_async

from nb_cli_plugin_webui.i18n import _
from nb_cli_plugin_webui.app.config import CONFIG_FILE, Config
from nb_cli_plugin_webui.app.handlers.project import PROJECT_DATA_PATH


@click.group(
    cls=ClickAliasedGroup,
    invoke_without_command=True,
    help=_("Prepare operations related to docker."),
)
@click.pass_context
@run_async
async def docker(ctx: click.Context):
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


# TODO: docker up


@docker.command(help=_("Copy config and data file in current directory for docker."))
@run_async
async def copy():
    cwd = Path.cwd()

    try:
        Config.store(cwd / CONFIG_FILE)
    except Exception as e:
        click.secho(str(e), fg="red")
        return

    try:
        shutil.copy(PROJECT_DATA_PATH, cwd / PROJECT_DATA_PATH.name)
    except Exception as e:
        click.secho(str(e), fg="red")
        return

    click.secho(_("Config and data file copied successfully."), fg="green")
