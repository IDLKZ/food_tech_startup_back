import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped,relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.shared.infrastructure.models.base_model import Base
from app.shared.infrastructure.models.shared_table_names import SharedTableNames
from app.shared.infrastructure.models.shared_model_names import SharedModelNames


class UserOrganizationModel(Base):
    __tablename__ = SharedTableNames.UserOrganizationTableName

    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(f"{SharedTableNames.UserTableName}.id", ondelete="CASCADE"),
        primary_key=True,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(f"{SharedTableNames.OrganizationTableName}.id", ondelete="CASCADE"),
        primary_key=True,
    )

    __table_args__ = (
        UniqueConstraint("user_id", "organization_id", name="uix_user_organizations"),
    )

    # Связки
    user: Mapped[SharedModelNames.UserModelName] = relationship(back_populates="organizations")  # noqa: F821
    organization: Mapped[SharedModelNames.OrganizationModelName] = relationship(back_populates="users")  # noqa: F821