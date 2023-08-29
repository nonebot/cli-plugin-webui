from pathlib import Path

from jinja2 import Environment, FileSystemLoader

templates = Environment(
    trim_blocks=True,
    lstrip_blocks=True,
    autoescape=False,
    enable_async=True,
    loader=FileSystemLoader(Path(__file__).parent.parent.parent / "template"),
)
