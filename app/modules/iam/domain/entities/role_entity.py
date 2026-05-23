import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid_utils import uuid7
from app.core.exceptions.common_exceptions import ApiNotFoundException
from app.modules.iam.domain.value_objects.role_value import RoleValue
from app.modules.iam.domain.events.role_events.role_events import (
    RoleCreatedEvent,
    RoleUpdatedEvent,
    RoleDeletedEvent,
    RolePermissionGrantedEvent,
    RolePermissionRevokedEvent,
)
from app.shared.domain.entity.base_aggregator import AggregateRoot


@dataclass
class RoleEntity(AggregateRoot):
    id: uuid.UUID
    title_ru: str
    value: RoleValue
    title_kk: Optional[str] = None
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None
    permission_ids: list[uuid.UUID] = field(default_factory=list)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    deleted_at: Optional[datetime] = None

    # ── фабричный метод ───────────────────────────────────────────
    @classmethod
    def create(
        cls,
        title_ru: str,
        value: str,
        title_kk: Optional[str] = None,
        title_en: Optional[str] = None,
        description_ru: Optional[str] = None,
        description_kk: Optional[str] = None,
        description_en: Optional[str] = None,
    ) -> "RoleEntity":
        role = cls(
            id=uuid.UUID(str(uuid7())),
            title_ru=title_ru,
            title_kk=title_kk,
            title_en=title_en,
            description_ru=description_ru,
            description_kk=description_kk,
            description_en=description_en,
            value=RoleValue(value),   # ← валидация здесь
        )
        role.add_event(RoleCreatedEvent(
            role_id=role.id,
            value=str(role.value),
        ))
        return role

    # ── бизнес методы ─────────────────────────────────────────────

    def update(
        self,
        title_ru: str,
        title_kk: Optional[str] = None,
        title_en: Optional[str] = None,
        description_ru: Optional[str] = None,
        description_kk: Optional[str] = None,
        description_en: Optional[str] = None,
    ) -> None:
        self.title_ru = title_ru
        self.title_kk = title_kk
        self.title_en = title_en
        self.description_ru = description_ru
        self.description_kk = description_kk
        self.description_en = description_en
        self._touch()
        self.add_event(RoleUpdatedEvent(role_id=self.id))

    def grant_permission(self, permission_id: uuid.UUID) -> None:
        if permission_id in self.permission_ids:
            raise ApiNotFoundException()
        self.permission_ids.append(permission_id)
        self._touch()
        self.add_event(RolePermissionGrantedEvent(
            role_id=self.id,
            permission_id=permission_id,
        ))

    def revoke_permission(self, permission_id: uuid.UUID) -> None:
        if permission_id not in self.permission_ids:
            raise ApiNotFoundException()
        self.permission_ids.remove(permission_id)
        self._touch()
        self.add_event(RolePermissionRevokedEvent(
            role_id=self.id,
            permission_id=permission_id,
        ))

    def soft_delete(self) -> None:
        self.deleted_at = datetime.now(timezone.utc)
        self._touch()
        self.add_event(RoleDeletedEvent(role_id=self.id))

    def has_permission(self, permission_id: uuid.UUID) -> bool:
        return permission_id in self.permission_ids

    # ── свойства ──────────────────────────────────────────────────

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def _touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)