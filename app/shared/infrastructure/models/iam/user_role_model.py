import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped,relationship

from app.shared.infrastructure.models.base_model import Base
from app.shared.infrastructure.models.shared_table_names import SharedTableNames
from app.shared.infrastructure.models.shared_model_names import SharedModelNames
from sqlalchemy.dialects.postgresql import UUID as PGUUID

class UserRoleModel(Base):
    __tablename__ = SharedTableNames.UserRolesTableName

    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(f"{SharedTableNames.UserTableName}.id", ondelete="CASCADE"),
        primary_key=True,
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(f"{SharedTableNames.RoleTableName}.id", ondelete="CASCADE"),
        primary_key=True,
    )

    # ограничение уникальности
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uix_user_roles"),
    )
    # Связки
    user: Mapped[SharedModelNames.UserModelName] = relationship(back_populates="roles")  # noqa: F821
    role: Mapped[SharedModelNames.RoleModelName] = relationship(back_populates="users")  # noqa: F821