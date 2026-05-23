import uuid

from sqlalchemy import UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.shared.infrastructure.models.base_model import Base
from app.shared.infrastructure.models.shared_table_names import SharedTableNames
from app.shared.infrastructure.models.shared_model_names import SharedModelNames

class RolePermissionModel(Base):
    __tablename__ =  SharedTableNames.RolePermissionTableName

    role_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(f"{SharedTableNames.RoleTableName}.id", ondelete="CASCADE"),
        primary_key=True,
    )
    permission_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(f"{SharedTableNames.PermissionTableName}.id", ondelete="CASCADE"),
        primary_key=True,
    )

    # ограничение уникальности
    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="uix_role_permission"),
    )
    #Связки
    role: Mapped[SharedModelNames.RoleModelName] = relationship(back_populates="permissions")  # noqa: F821
    permission: Mapped[SharedModelNames.PermissionModelName] = relationship(back_populates="roles")  # noqa: F821
