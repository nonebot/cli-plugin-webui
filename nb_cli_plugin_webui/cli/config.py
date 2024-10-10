from enum import Enum
from typing import List, cast

import click
from nb_cli.i18n import _ as nb_cli_i18n
from noneprompt import Choice, ListPrompt, InputPrompt, CancelledError
from nb_cli.cli import CLI_DEFAULT_STYLE, ClickAliasedGroup, run_sync, run_async

from nb_cli_plugin_webui.i18n import _
from nb_cli_plugin_webui.app.config import CONFIG_FILE_PATH, Config

DISABLED_CONFIG = ["hashed_token", "salt", "secret_key"]


@click.group(
    cls=ClickAliasedGroup,
    invoke_without_command=True,
    help=_("Setting NoneBot CLI WebUI."),
)
@click.pass_context
@run_async
async def config(ctx: click.Context):
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
            question=nb_cli_i18n("What do you want to do?"),
            choices=choices,
        ).prompt_async(style=CLI_DEFAULT_STYLE)
    except CancelledError:
        ctx.exit()

    sub_cmd = result.data
    await run_sync(ctx.invoke)(sub_cmd)


@config.command(help=_("List config."))
@run_async
async def list_():
    click.secho(_(f"Config file path: {CONFIG_FILE_PATH}"), fg="green")
    for key, value in Config.dict().items():
        if isinstance(value, Enum):
            value = value.value
        click.secho(f"{key}: {value}")


@config.command(help=_("Setting config."))
@click.option(
    "-k",
    "--key",
    type=str,
    help=_("The key of config."),
)
@click.option(
    "-v",
    "--value",
    type=str,
    help=_("The value of config."),
)
@run_async
async def set(key: str, value: str):
    conf_key = key
    conf_value = value

    if not conf_key:
        conf_key = await InputPrompt(_("Please enter key:")).prompt_async(
            style=CLI_DEFAULT_STYLE
        )
    if conf_key in DISABLED_CONFIG:
        click.secho(_("Key is disabled."))
        return
    if not conf_value:
        conf_value = await InputPrompt(_("Please enter value:")).prompt_async(
            style=CLI_DEFAULT_STYLE
        )

    conf = Config

    if conf.dict().get(conf_key) is None:
        click.secho(_("Invalid key."))
        return

    if conf_key == "allowed_origins":
        conf_value = conf_value.split(",")

    click.secho(_("Change log:"))
    click.secho(
        _("Old: {conf_key} = {conf_value}").format(
            conf_key=conf_key, conf_value=conf.dict()[conf_key]
        )
    )
    click.secho(
        _("New: {conf_key} = {conf_value}").format(
            conf_key=conf_key, conf_value=conf_value
        )
    )

    setattr(conf, conf_key, conf_value)
    conf.store(CONFIG_FILE_PATH)

    click.secho(_("Config set successfully."), fg="green")
