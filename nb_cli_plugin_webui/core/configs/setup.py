from pathlib import Path

import click
from pydantic import SecretStr
from nb_cli.cli import CLI_DEFAULT_STYLE
from noneprompt import InputPrompt, ConfirmPrompt

from nb_cli_plugin_webui.i18n import _
from nb_cli_plugin_webui.core.configs.config import config
from nb_cli_plugin_webui.exceptions import TokenComplexityError
from nb_cli_plugin_webui.models.domain.config import WebUIConfig
from nb_cli_plugin_webui.utils import check_token_complexity, generate_complexity_string


async def get_user_config():
    click.secho(_("Welcome to use NB CLI WebUI."), fg="green")
    click.secho("")
    click.secho(_("[Token Setting]"), fg="green")
    click.secho(_("Token is your key to access WebUI."))
    if await ConfirmPrompt(_("Do you want it generated?")).prompt_async(
        style=CLI_DEFAULT_STYLE
    ):
        token = generate_complexity_string(use_digits=True, use_punctuation=True)
    else:
        token = await InputPrompt(_("Please enter token:")).prompt_async(
            style=CLI_DEFAULT_STYLE
        )
        while True:
            try:
                check_token_complexity(token)
                break
            except TokenComplexityError as err:
                click.secho(str(err))

            token = await InputPrompt(_("Please enter again:")).prompt_async(
                style=CLI_DEFAULT_STYLE
            )

    click.secho(_("Your token is:"))
    click.secho(f"\n{token}\n", fg="green")
    click.secho(_("ATTENTION, TOKEN ONLY SHOW ONCE."), fg="red", bold=True)

    click.secho("")
    click.secho(_("[Server Setting]"), fg="green")
    host = "localhost"
    port = "12345"
    if await ConfirmPrompt(
        _("Do you want to decide (host) and (port) by yourself?")
    ).prompt_async(style=CLI_DEFAULT_STYLE):
        host = await InputPrompt(_("Please enter host:")).prompt_async(
            style=CLI_DEFAULT_STYLE
        )
        port = await InputPrompt(_("Please enter port:")).prompt_async(
            style=CLI_DEFAULT_STYLE
        )
        while True:
            try:
                if int(port) < 0 or int(port) > 65535:
                    raise ValueError
                break
            except ValueError:
                click.secho(_("Port must be between 0 and 65535."))
                port = await InputPrompt(_("Please enter port:")).prompt_async(
                    style=CLI_DEFAULT_STYLE
                )

        click.secho(_("Your webui url is:"))
        click.secho(f"\nhttp://{host}:{port}/\n", fg="green")
    else:
        click.secho(_("Your webui url will decide by nb-cli."))

    click.secho("")
    click.secho(_("[General Setting]"), fg="green")
    click.secho(_("BASE DIR REQUIRE"), fg="red")
    click.secho(_("- Absolute path. Example:"))
    click.secho(("  * Linux: /home/(user)/"))
    click.secho(("  * MacOS: /Users/(user)/"))
    click.secho(("  * Windows: C:/Users/Public/Pictures"))
    click.secho(_("- NoneBot instance will be stored here."))
    click.secho(
        _("- The base directory for WebUI file system display will start here."),
        fg="red",
    )
    click.secho(_("- The path entered will be validated to ensure it exists"), fg="red")
    base_dir = await InputPrompt(_("Please enter base dir:")).prompt_async(
        style=CLI_DEFAULT_STYLE
    )
    while True:
        if not Path(base_dir).exists():
            click.secho(_("This directory does not exist."))
            base_dir = await InputPrompt(_("Please enter again:")).prompt_async(
                style=CLI_DEFAULT_STYLE
            )
        else:
            break

    click.secho("")
    click.secho(_("[Setting Overview]"), fg="green")
    click.secho(_(f"Token: {token}"))
    click.secho(_(f"WebUI URL: http://{host}:{port}/"))
    click.secho(_(f"Base DIR: {base_dir}"))
    if not await ConfirmPrompt(_("Are you confirm?")).prompt_async(
        style=CLI_DEFAULT_STYLE
    ):
        return

    user_config = WebUIConfig(
        host=host,
        port=port,
        secret_key=SecretStr(
            generate_complexity_string(32, use_digits=True, use_punctuation=True)
        ),
        base_dir=base_dir,
    )
    user_config.reset_token(token)

    config.store(user_config)
