# app/shared/domain/base_aggregate.py
from dataclasses import dataclass, field
from app.shared.domain.event.base_domain_event import DomainEvent


@dataclass
class AggregateRoot:
    _events: list[DomainEvent] = field(
        default_factory=list,
        init=False,
        repr=False,
    )

    def add_event(self, event: DomainEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events

    def has_events(self) -> bool:
        return len(self._events) > 0