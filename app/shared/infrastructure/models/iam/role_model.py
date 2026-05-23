from sqlalchemy.orm import Mapped,relationship

from app.shared.infrastructure.models.base_model import FullBase
from app.shared.infrastructure.models.shared_model_columns import SharedModelColumns
from app.shared.infrastructure.models.shared_table_names import SharedTableNames
from app.shared.infrastructure.models.shared_model_names import SharedModelNames

class RoleModel(FullBase):
    __tablename__ = SharedTableNames.RoleTableName
    #Наименование ролей
    title_ru: Mapped[SharedModelColumns.StandardTitle("Название роли на русском", nullable=False)]
    title_kk: Mapped[SharedModelColumns.StandardTitle("Название роли на казахском", nullable=True)]
    title_en: Mapped[SharedModelColumns.StandardTitle("Название роли на английском", nullable=True)]

    #Описание ролей
    description_ru: Mapped[SharedModelColumns.StandardTextDescription("Описание роли на русском", nullable=True)]
    description_kk: Mapped[SharedModelColumns.StandardTextDescription("Описание роли на казахском", nullable=True)]
    description_en: Mapped[SharedModelColumns.StandardTextDescription("Описание роли на английском", nullable=True)]

    #Уникальное значение ролей
    value: Mapped[SharedModelColumns.StandardUniqueValue("Уникальное значение роли")]

    #Ключи связки
    permissions: Mapped[list[SharedModelNames.RolePermissionModelName]] = relationship(  # noqa: F821
        back_populates="role",
        cascade="all, delete-orphan"
    )
    users: Mapped[list[SharedModelNames.UserRoleModelName]] = relationship(  # noqa: F821
        back_populates="role",
        cascade="all, delete-orphan"
    )