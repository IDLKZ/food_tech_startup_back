from sqlalchemy.orm import Mapped, relationship

from app.shared.infrastructure.models.base_model import FullBase
from app.shared.infrastructure.models.shared_model_columns import SharedModelColumns
from app.shared.infrastructure.models.shared_model_names import SharedModelNames
from app.shared.infrastructure.models.shared_table_names import SharedTableNames


class OrganizationModel(FullBase):
    __tablename__ = SharedTableNames.OrganizationTableName

    # Наименование
    full_name: Mapped[SharedModelColumns.StandardTitle("Полное название организации", nullable=False)]
    short_name: Mapped[SharedModelColumns.StandardTitle("Краткое название организации", nullable=True)]

    # Контакты
    address: Mapped[SharedModelColumns.StandardTitle("Адрес организации", nullable=True)]
    phone: Mapped[SharedModelColumns.Phone(nullable=True)]
    email: Mapped[SharedModelColumns.Email(nullable=True)]

    # Реквизиты
    bin: Mapped[SharedModelColumns.StandardUniqueBINValue("БИН организации")]

    # Статус
    is_active: Mapped[SharedModelColumns.CheckBool(comment="Организация активна", nullable=False, default=True)]

    # Связки
    users: Mapped[list[SharedModelNames.UserOrganizationModelName]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan"
    )