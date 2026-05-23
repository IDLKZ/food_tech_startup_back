import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid_utils import uuid7


@dataclass(frozen=True)
class DomainEvent:
    event_id: uuid.UUID = field(
        default_factory=lambda: uuid.UUID(str(uuid7())),
        kw_only=True,
    )
    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
        kw_only=True,
    )