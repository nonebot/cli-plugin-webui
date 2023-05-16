from typing import cast

from nb_cli.cli import CLIMainGroup, cli

from nb_cli_plugin_webui.cli import webui


def install():
    cli_ = cast(CLIMainGroup, cli)
    cli_.add_command(webui)
    cli_.add_aliases("webui", ["ui"])
