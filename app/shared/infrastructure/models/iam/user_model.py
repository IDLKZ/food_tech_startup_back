from sqlalchemy.orm import Mapped,relationship

from app.shared.infrastructure.models.base_model import FullBase
from app.shared.infrastructure.models.shared_model_columns import SharedModelColumns
from app.shared.infrastructure.models.shared_table_names import SharedTableNames
from app.shared.infrastructure.models.shared_model_names import SharedModelNames


class UserModel(FullBase):
    __tablename__ = SharedTableNames.UserTableName
    #ФИО
    first_name: Mapped[SharedModelColumns.FIO("Имя", nullable=False)]
    last_name: Mapped[SharedModelColumns.FIO("Фамилия", nullable=False)]
    patronymic: Mapped[SharedModelColumns.FIO("Отчество", nullable=True)]
    #Данные для входа и идентификации
    username: Mapped[SharedModelColumns.Username(nullable=False, unique=True, index=True)]
    email: Mapped[SharedModelColumns.Email(nullable=False, unique=True, index=True)]
    phone: Mapped[SharedModelColumns.Phone(nullable=False, unique=True, index=True)]
    #Данные о пользователе (др, пол, фото)
    gender: Mapped[SharedModelColumns.Gender(comment="Пол 0 - не определен, 1 - Мужской, 2 - Женский", nullable=False)]
    birthdate: Mapped[SharedModelColumns.OnlyDate(comment="Дата рождения", nullable=True)]
    image: Mapped[SharedModelColumns.Image("Аватар пользователя", nullable=True)]
    password_hash: Mapped[SharedModelColumns.Password(comment="Пароль", nullable=False, default=None)]
    #Статусы
    is_active: Mapped[SharedModelColumns.CheckBool(comment="Пользователь активен", nullable=False, default=True)]
    is_verified: Mapped[SharedModelColumns.CheckBool(comment="Пользователь верифицирован", nullable=False, default=False)]
    #Данные последнего входа
    last_seen_at: Mapped[SharedModelColumns.Datetime(comment="Последний раз был активен", nullable=True, useTimezone=True)]

    #Связанные данные
    groups: Mapped[list[SharedModelNames.UserGroupModelName]] = relationship(  # noqa: F821
        back_populates="user",
        cascade="all, delete-orphan"
    )

    roles: Mapped[list[SharedModelNames.UserRoleModelName]] = relationship(  # noqa: F821
        back_populates="user",
        cascade="all, delete-orphan"
    )

    organizations: Mapped[list[SharedModelNames.UserOrganizationModelName]] = relationship(  # noqa: F821
        back_populates="user",
        cascade="all, delete-orphan"
    )

