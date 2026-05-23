# app/modules/iam/domain/value_objects/role_value.py
import re
from dataclasses import dataclass

from app.core.exceptions.common_exceptions import ApiBadRequestException
from app.core.locales.locale_keys import LocaleKeys


@dataclass(frozen=True)
class RoleValue:
    value: str

    def __post_init__(self) -> None:
        clean = self.value.strip().lower()
        if not re.match(r"^[a-z][a-z0-9_]*$", clean):
            raise ApiBadRequestException(LocaleKeys.ROLE_ALREADY_EXISTS)
        if len(clean) < 2 or len(clean) > 50:
            raise ApiBadRequestException(LocaleKeys.ROLE_ALREADY_EXISTS)
        object.__setattr__(self, "value", clean)

    def __str__(self) -> str:
        return self.value