from typing import List, cast

import click
from nb_cli.i18n import _ as nb_cli_i18n
from noneprompt import Choice, ListPrompt, InputPrompt, CancelledError
from nb_cli.cli import CLI_DEFAULT_STYLE, ClickAliasedGroup, run_sync, run_async

from nb_cli_plugin_webui.i18n import _
from nb_cli_plugin_webui.utils import (
    find_available_port,
    check_token_complexity,
    generate_complexity_string,
)


@click.group(
    cls=ClickAliasedGroup, invoke_without_command=True, help=_("Start NB CLI WebUI.")
)
@click.option(
    "-h",
    "--host",
    type=str,
    show_default=True,
    help=_("The host required to access NB CLI WebUI."),
    default="localhost",
)
@click.option(
    "-p",
    "--port",
    type=int,
    show_default=True,
    help=_("The port required to access NB CLI WebUI."),
    default=find_available_port(10000, 20000),
)
@click.pass_context
@run_async
async def webui(ctx: click.Context, host: str, port: int):
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


@webui.command(help=_("Run NB CLI WebUI"))
@run_async
async def start():
    ...


@webui.command(help=_("Set access Token."))
@run_async
async def setting_token():
    att = await InputPrompt(_("Do you want it generated? [Y/N]")).prompt_async(
        style=CLI_DEFAULT_STYLE
    )
    if att in ["y", "Y"]:
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

    click.secho(_(f"Your token is:"))
    click.secho(f"\n{token}\n", fg="green")
    click.secho(_("ATTENTION, TOKEN ONLY SHOW ONCE."), fg="red")

    secret_key = generate_complexity_string(length=18)
    # TODO ...
