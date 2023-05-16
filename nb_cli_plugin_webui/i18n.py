import gettext
from pathlib import Path

from nb_cli.i18n import get_locale

t = gettext.translation(
    "webui",
    localedir=Path(__file__).parent / "locale",
    languages=[lang] if (lang := get_locale()) else None,
    fallback=True,
)

_ = t.gettext
