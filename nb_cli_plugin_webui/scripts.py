import sys
import json
import subprocess

import httpx
from babel.messages.frontend import CommandLineInterface

from nb_cli_plugin_webui import get_version


def extract():
    version = get_version()
    CommandLineInterface().run(
        [
            "pybabel",
            "extract",
            "-o",
            "messages.pot",
            "--project",
            "nb-cli-plugin-webui",
            "--version",
            version,
            "nb_cli_plugin_webui/",
        ]
    )


def init():
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: poetry run init <lang>")
        exit(-1)

    extract()

    CommandLineInterface().run(
        [
            "pybabel",
            "init",
            "-D",
            "nb-cli-plugin-webui",
            "-i",
            "messages.pot",
            "-d",
            "nb_cli_plugin_webui/locale",
            "-l",
            args[0],
        ]
    )


def update():
    extract()
    CommandLineInterface().run(
        [
            "pybabel",
            "update",
            "-D",
            "nb-cli-plugin-webui",
            "-i",
            "messages.pot",
            "-d",
            "nb_cli_plugin_webui/locale",
        ]
    )


def compile():
    CommandLineInterface().run(
        [
            "pybabel",
            "compile",
            "-D",
            "nb-cli-plugin-webui",
            "-d",
            "nb_cli_plugin_webui/locale",
        ]
    )


def _get_openapi():
    args = sys.argv[1:]
    if len(args) != 2:
        print("Usage: poetry run generate <host> <port>")
        exit(-1)

    host = args[0]
    port = args[1]
    url = f"http://{host}:{port}/api/docs/openapi.json"
    response = httpx.get(url, proxies=dict())
    if response.status_code == 502:
        print("Error: Could not fetch OpenAPI schema")
        exit(-1)

    with open("./openapi.json", "w") as f:
        f.write(json.dumps(response.json()))


def generate_openapi():
    _get_openapi()
    subprocess.run(
        [
            "pnpm",
            "-r",
            "openapi-ts",
        ]
    )
