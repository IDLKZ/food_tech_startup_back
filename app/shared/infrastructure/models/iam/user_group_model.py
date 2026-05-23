import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.shared.infrastructure.models.base_model import  Base
from app.shared.infrastructure.models.shared_table_names import SharedTableNames
from app.shared.infrastructure.models.shared_model_names import SharedModelNames


class UserGroupModel(Base):
    __tablename__ = SharedTableNames.UserGroupsTableName

    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(f"{SharedTableNames.UserTableName}.id", ondelete="CASCADE"),
        primary_key=True,
    )
    group_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(f"{SharedTableNames.GroupTableName}.id", ondelete="CASCADE"),
        primary_key=True,
    )

    # ограничение уникальности
    __table_args__ = (
        UniqueConstraint("user_id", "group_id", name="uix_user_groups"),
    )
    # Связки
    user: Mapped[SharedModelNames.UserModelName] = relationship(back_populates="groups")  # noqa: F821
    group: Mapped[SharedModelNames.GroupModelName] = relationship(back_populates="users")  # noqa: F821