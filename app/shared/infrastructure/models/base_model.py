import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from uuid_utils import uuid7, UUID


class Base(DeclarativeBase):
    pass


class UUIDBase(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=lambda: uuid.UUID(str(uuid7())),
        nullable=False,
    )


class TimestampMixin:
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # БД ставит время при INSERT
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # БД ставит время при INSERT
        onupdate=func.now(),        # БД обновляет при UPDATE
        nullable=False,
    )


class SoftDeleteMixin:
    __abstract__ = True

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,  # None — просто Python default, не вызов функции
    )

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None


class UUIDTimestampBase(UUIDBase, TimestampMixin):
    __abstract__ = True


class FullBase(UUIDBase, TimestampMixin, SoftDeleteMixin):
    __abstract__ = True