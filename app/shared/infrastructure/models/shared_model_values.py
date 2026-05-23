from typing import Final


class SharedModelValues:
    # Длина общих полей
    TITLE_MAX_LENGTH:Final[int] = 250
    UNIQUE_VALUE_MAX_LENGTH:Final[int] = 280
    # Юридические данные
    BIN_LENGTH:Final[int] = 12
    IIN_LENGTH:Final[int]= 12
    # Цена
    PRICE_PRECISION:Final[int] = 20
    PRICE_SCALE:Final[int] = 2
    # Контакты
    PHONE_LENGTH:Final[int] = 50
    FIO_LENGTH:Final[int] = 100
    IMAGE_LENGTH:Final[int] = 500
    PASSWORD_LENGTH:Final[int] = 250
    EMAIL_LENGTH:Final[int] = 250
    USERNAME_LENGTH:Final[int] = 50
    # Пол
    GENDER_UNDEFINED:Final[int] = 0
    GENDER_MALE:Final[int] = 1
    GENDER_FEMALE:Final[int] = 2
    OPTIONAL_GENDERS: frozenset = frozenset({GENDER_UNDEFINED, GENDER_MALE, GENDER_FEMALE})