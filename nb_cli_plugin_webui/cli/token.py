from typing import List, cast

import click
from nb_cli.i18n import _ as nb_cli_i18n
from nb_cli.cli import CLI_DEFAULT_STYLE, ClickAliasedGroup, run_sync, run_async
from noneprompt import Choice, ListPrompt, InputPrompt, ConfirmPrompt, CancelledError

from nb_cli_plugin_webui.i18n import _
from nb_cli_plugin_webui.app.config import CONFIG_FILE_PATH, Config
from nb_cli_plugin_webui.app.utils.string_utils import (
    check_string_complexity,
    generate_complexity_string,
)

conf = Config


@click.group(
    cls=ClickAliasedGroup,
    invoke_without_command=True,
    help=_("Manage NoneBot WebUI access token."),
)
@click.pass_context
@run_async
async def token(ctx: click.Context):
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


@token.command(help=_("Reset access token."))
@run_async
async def reset():
    if await ConfirmPrompt(_("Generate a new access token?")).prompt_async(
        style=CLI_DEFAULT_STYLE
    ):
        token = generate_complexity_string(use_digits=True, use_punctuation=True)
    else:
        while True:
            token = await InputPrompt(_("Please enter new access token:")).prompt_async(
                style=CLI_DEFAULT_STYLE
            )

            try:
                check_string_complexity(token)
                break
            except Exception as e:
                click.secho(str(e), fg="red")

    click.secho(_("New access token: {token}").format(token=token), fg="green")
    click.secho(
        _(
            "Please remember the access token, "
            "you will not be able to retrieve it again."
        ),
        fg="yellow",
    )
    conf.reset_token(token)
    conf.store(CONFIG_FILE_PATH)
