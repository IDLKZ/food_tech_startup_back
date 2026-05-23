from enum import StrEnum


class LocaleKeys(StrEnum):
    INVALID_CREDENTIALS = "invalid_credentials"
    USER_NOT_FOUND = "user_not_found"
    USER_ALREADY_EXISTS = "user_already_exists"
    USER_BLOCKED = "user_blocked"
    USER_NOT_VERIFIED = "user_not_verified"

    INVALID_EMAIL = "invalid_email"
    INVALID_PHONE = "invalid_phone"
    INVALID_USERNAME = "invalid_username"
    INVALID_PASSWORD = "invalid_password"

    ROLE_NOT_FOUND = "role_not_found"
    ROLE_ALREADY_EXISTS = "role_already_exists"
    PERMISSION_NOT_FOUND = "permission_not_found"
    PERMISSION_ALREADY_GRANTED = "permission_already_granted"

    NOT_FOUND = "not_found"
    ALREADY_EXISTS = "already_exists"
    FORBIDDEN = "forbidden"
    VALIDATION_ERROR = "validation_error"
    INTERNAL_ERROR = "internal_error"
    BAD_REQUEST = "bad_request"