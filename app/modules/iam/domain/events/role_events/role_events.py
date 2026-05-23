# app/modules/iam/domain/events/role_events.py
from dataclasses import dataclass
from uuid import UUID

from app.shared.domain.event.base_domain_event import DomainEvent


@dataclass(frozen=True)
class RoleCreatedEvent(DomainEvent):
    role_id: UUID
    value: str


@dataclass(frozen=True)
class RoleUpdatedEvent(DomainEvent):
    role_id: UUID


@dataclass(frozen=True)
class RoleDeletedEvent(DomainEvent):
    role_id: UUID


@dataclass(frozen=True)
class RolePermissionGrantedEvent(DomainEvent):
    role_id: UUID
    permission_id: UUID


@dataclass(frozen=True)
class RolePermissionRevokedEvent(DomainEvent):
    role_id: UUID
    permission_id: UUID