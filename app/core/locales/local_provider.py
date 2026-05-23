import gettext
import os
from functools import lru_cache

LOCALES_DIR = os.path.join(os.path.dirname(__file__), "..", "locales")
SUPPORTED_LANGS = ("ru", "kk", "en")
DEFAULT_LANG = "ru"

@lru_cache(maxsize=3)
def _get_translator(lang: str) -> gettext.GNUTranslations:
    try:
        return gettext.translation(
            domain="messages",
            localedir=LOCALES_DIR,
            languages=[lang],
        )
    except FileNotFoundError:
        return gettext.translation(
            domain="messages",
            localedir=LOCALES_DIR,
            languages=[DEFAULT_LANG],
        )


def translate(message_key: str, lang: str = "ru", *args) -> str:
    text = _get_translator(lang).gettext(message_key)
    if args:
        return text % args
    return text