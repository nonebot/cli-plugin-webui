import webbrowser
from typing import List, cast

import click
from pydantic import SecretStr
from nb_cli.i18n import _ as nb_cli_i18n
from nb_cli.cli import CLI_DEFAULT_STYLE, ClickAliasedGroup, run_sync, run_async
from noneprompt import Choice, ListPrompt, InputPrompt, ConfirmPrompt, CancelledError

from nb_cli_plugin_webui.i18n import _
from nb_cli_plugin_webui.core import server
from nb_cli_plugin_webui.core.config import WebUIConfig, config
from nb_cli_plugin_webui.utils import (
    find_available_port,
    check_token_complexity,
    generate_complexity_string,
)


@click.group(
    cls=ClickAliasedGroup, invoke_without_command=True, help=_("Start NB CLI UI.")
)
@click.pass_context
@run_async
async def webui(ctx: click.Context):
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


@webui.command(help=_("Run NB CLI UI"))
@click.option(
    "-h",
    "--host",
    type=str,
    show_default=True,
    help=_("The host required to access NB CLI UI."),
    default="localhost",
)
@click.option(
    "-p",
    "--port",
    type=int,
    show_default=True,
    help=_("The port required to access NB CLI UI."),
    default=find_available_port(10000, 20000),
)
@run_async
async def start(host: str, port: int):
    webbrowser.open(f"http://{host}:{port}/")
    await server.run_server(host, port)


@webui.command(help=_("Reset or create access Token."))
@run_async
async def setting_token():
    if config.exist:
        if not await ConfirmPrompt(
            _("Token is exist, did you need overwrite?")
        ).prompt_async(style=CLI_DEFAULT_STYLE):
            return
    else:
        click.secho(_("Token is not exist."))

    if await ConfirmPrompt(_("Do you want it generated?")).prompt_async(
        style=CLI_DEFAULT_STYLE
    ):
        token = generate_complexity_string()
    else:
        token = await InputPrompt(_("Please enter token:")).prompt_async(
            style=CLI_DEFAULT_STYLE
        )
        while True:
            try:
                check_token_complexity(token)
                break
            except Exception as err:
                click.secho(str(err))

            token = await InputPrompt(_("Please enter again:")).prompt_async(
                style=CLI_DEFAULT_STYLE
            )

    click.secho(_("Your token is:"))
    click.secho(f"\n{token}\n", fg="green")
    click.secho(_("ATTENTION, TOKEN ONLY SHOW ONCE."), fg="red", bold=True)

    if config.exist:
        cache = config.read()
        cache.reset_token(token)
        config.store(cache)
    else:
        user_config = WebUIConfig(
            secret_key=SecretStr(generate_complexity_string(18)),
            is_customize=False,
        )
        user_config.reset_token(token)
        config.store(user_config)
