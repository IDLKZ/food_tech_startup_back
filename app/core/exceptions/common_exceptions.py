from app.core.exceptions.app_exception import AppException
from app.core.locales.locale_keys import LocaleKeys


class ApiBadRequestException(AppException):
    def __init__(
        self,
        message_key: LocaleKeys = LocaleKeys.BAD_REQUEST,
        *args,
        inner_code: int | None = 400,
    ):
        super().__init__(
            message_key, *args,
            inner_code=inner_code,
            status_code=400,
        )


class ApiNotFoundException(AppException):
    def __init__(
        self,
        message_key: LocaleKeys = LocaleKeys.NOT_FOUND,
        *args,
        inner_code: int | None = 404,
    ):
        super().__init__(
            message_key, *args,
            inner_code=inner_code,
            status_code=404,
        )


class ApiForbiddenException(AppException):
    def __init__(
        self,
        message_key: LocaleKeys = LocaleKeys.FORBIDDEN,
        *args,
        inner_code: int | None = 403,
    ):
        super().__init__(
            message_key, *args,
            inner_code=inner_code,
            status_code=403,
        )


class ApiUnauthorizedException(AppException):
    def __init__(
        self,
        message_key: LocaleKeys = LocaleKeys.INVALID_CREDENTIALS,
        *args,
        inner_code: int | None = 401,
    ):
        super().__init__(
            message_key, *args,
            inner_code=inner_code,
            status_code=401,
        )


class ApiConflictException(AppException):
    def __init__(
        self,
        message_key: LocaleKeys = LocaleKeys.ALREADY_EXISTS,
        *args,
        inner_code: int | None = 409,
    ):
        super().__init__(
            message_key, *args,
            inner_code=inner_code,
            status_code=409,
        )


class ApiValidationException(AppException):
    def __init__(
        self,
        message_key: LocaleKeys = LocaleKeys.VALIDATION_ERROR,
        *args,
        inner_code: int | None = 422,
    ):
        super().__init__(
            message_key, *args,
            inner_code=inner_code,
            status_code=422,
        )