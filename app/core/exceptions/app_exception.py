from typing import Any

from app.core.locales.locale_keys import LocaleKeys


class AppException(Exception):
    def __init__(
        self,
        message_key: LocaleKeys = LocaleKeys.BAD_REQUEST,
        *args: Any,
        inner_code: int | None = None,
        status_code: int = 400,
    ) -> None:
        self.message_key = message_key
        self.args_values = args          # для форматирования строки
        self.inner_code = inner_code or status_code
        self.status_code = status_code
        super().__init__(message_key)