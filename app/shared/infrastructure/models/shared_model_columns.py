import datetime
from typing import Annotated, Optional
from sqlalchemy import String, Text, SmallInteger, Date, Boolean, DateTime
from sqlalchemy.orm import mapped_column, MappedColumn

from app.shared.infrastructure.models.shared_model_values import SharedModelValues


class SharedModelColumns:
    # Название
    @staticmethod
    def StandardTitle(
            comment: str | None = None,
            nullable: bool = False,
            index: bool = False,
            default: any = None
    ) -> type:
        py_type = str if not nullable else Optional[str]
        return Annotated[
            py_type,
            mapped_column(
                String(length=SharedModelValues.TITLE_MAX_LENGTH),
                nullable=nullable,
                index=index,
                default=default,
                comment=comment,
            ),
        ]

    # Описание
    @staticmethod
    def StandardTextDescription(
            comment: str | None = None,
            nullable: bool = False,
            default: any = None
    ) -> type:
        py_type = str if not nullable else Optional[str]
        return Annotated[
            py_type,
            mapped_column(
                Text(),
                nullable=nullable,
                default=default,
                comment=comment,
            ),
        ]

    # Уникальное значение
    @staticmethod
    def StandardUniqueValue(comment: str = "Уникальный код") -> type:
        return Annotated[str, mapped_column(
            String(length=SharedModelValues.UNIQUE_VALUE_MAX_LENGTH),
            unique=True,
            nullable=False,
            index=True,
            comment=comment,
        ),
    ]

    @staticmethod
    def StandardUniqueBINValue(comment: str = "Уникальный БИН") -> type:
        return Annotated[str, mapped_column(
            String(length=SharedModelValues.BIN_LENGTH),
            unique=True,
            nullable=False,
            index=True,
            comment=comment,
        ),
        ]

    @staticmethod
    def Image(comment: str = "S3 Фото", nullable: bool = False, default: any = None) -> type:
        py_type = str if not nullable else Optional[str]
        return Annotated[
            py_type,
            mapped_column(
                String(length=SharedModelValues.IMAGE_LENGTH),
                nullable=nullable,
                default=default,
                comment=comment,
            )
        ]

    @staticmethod
    def Password(comment: str = "Пароль", nullable: bool = False, default: any = None) -> type:
        py_type = str if not nullable else Optional[str]
        return Annotated[
            py_type,
            mapped_column(
                String(length=SharedModelValues.PASSWORD_LENGTH),
                nullable=nullable,
                default=default,
                comment=comment,
            )
        ]

    @staticmethod
    def FIO(comment: str = "ФИО",nullable: bool = False, default: any = None) -> type:
        py_type = str if not nullable else Optional[str]
        return Annotated[
            py_type,
            mapped_column(
                String(length=SharedModelValues.FIO_LENGTH),
                nullable=nullable,
                default=default,
                comment=comment,
            )
        ]

    @staticmethod
    def Email(comment: str = "Email",nullable: bool = False, default: any = None, unique: bool = False, index:bool=True) -> type:
        py_type = str if not nullable else Optional[str]
        return Annotated[
            py_type,
            mapped_column(
                String(length=SharedModelValues.EMAIL_LENGTH),
                nullable=nullable,
                default=default,
                unique=unique,
                index=index,
                comment=comment,
            )
        ]

    @staticmethod
    def Phone(comment: str = "Телефон", nullable: bool = False, default: any = None, unique: bool = False,
              index: bool = True) -> type:
        py_type = str if not nullable else Optional[str]
        return Annotated[
            py_type,
            mapped_column(
                String(length=SharedModelValues.PHONE_LENGTH),
                nullable=nullable,
                default=default,
                unique=unique,
                index=index,
                comment=comment,
            )
        ]

    @staticmethod
    def Username(comment: str = "Логин", nullable: bool = False, default: any = None, unique: bool = False,
              index: bool = True) -> type:
        py_type = str if not nullable else Optional[str]
        return Annotated[
            py_type,
            mapped_column(
                String(length=SharedModelValues.USERNAME_LENGTH),
                nullable=nullable,
                default=default,
                unique=unique,
                index=index,
                comment=comment,
            )
        ]

    @staticmethod
    def Gender(comment: str = "Пол", nullable: bool = False, default: int|None = SharedModelValues.GENDER_UNDEFINED)->type:
        py_type = int if not nullable else Optional[int]
        return  Annotated[
            py_type,
            mapped_column(
                SmallInteger,
                nullable=nullable,
                default=default,
                comment=comment,
            )
        ]

    @staticmethod
    def OnlyDate(comment: str = "Дата", nullable: bool = False) -> type:
        py_type = datetime.date if not nullable else Optional[datetime.date]
        return Annotated[
            py_type,
            mapped_column(
                Date,
                nullable=nullable,
                comment=comment,
            )
        ]

    @staticmethod
    def CheckBool(comment: str = "Логический оператор", nullable: bool = False, default: bool|None = None) -> type:
        py_type = bool if not nullable else Optional[bool]
        return Annotated[
            py_type,
            mapped_column(
                Boolean,
                nullable=nullable,
                default=default,
                comment=comment,
            )
        ]

    @staticmethod
    def Datetime(comment: str = "Дата и время", nullable: bool = False, useTimezone: bool = True) -> type:
        py_type = datetime.datetime if not nullable else Optional[datetime.datetime]
        return Annotated[
            py_type,
            mapped_column(
                DateTime(timezone=useTimezone),
                nullable=nullable,
                comment=comment,
            )
        ]
