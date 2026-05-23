from sqlalchemy.orm import Mapped, relationship

from app.shared.infrastructure.models.base_model import FullBase
from app.shared.infrastructure.models.shared_model_columns import SharedModelColumns
from app.shared.infrastructure.models.shared_table_names import SharedTableNames
from app.shared.infrastructure.models.shared_model_names import SharedModelNames

class GroupModel(FullBase):
    __tablename__ = SharedTableNames.GroupTableName
    # Наименование группы
    title_ru: Mapped[SharedModelColumns.StandardTitle("Название группы на русском", nullable=False)]
    title_kk: Mapped[SharedModelColumns.StandardTitle("Название группы на казахском", nullable=True)]
    title_en: Mapped[SharedModelColumns.StandardTitle("Название группы на английском", nullable=True)]

    # Описание группы
    description_ru: Mapped[SharedModelColumns.StandardTextDescription("Описание группы на русском", nullable=True)]
    description_kk: Mapped[SharedModelColumns.StandardTextDescription("Описание группы на казахском", nullable=True)]
    description_en: Mapped[SharedModelColumns.StandardTextDescription("Описание группы на английском", nullable=True)]

    # Уникальное значение группы пользователей
    value: Mapped[SharedModelColumns.StandardUniqueValue("Уникальное значение группы")]

    # Связанные данные
    users: Mapped[list[SharedModelNames.UserGroupModelName]] = relationship(  # noqa: F821
        back_populates="group",
        cascade="all, delete-orphan"
    )