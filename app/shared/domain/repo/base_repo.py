# app/shared/domain/base_repository.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional
from uuid import UUID

E = TypeVar("E")


class BaseRepo(ABC, Generic[E]):

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[E]: ...

    @abstractmethod
    async def get_all(self) -> list[E]: ...

    @abstractmethod
    async def save(self, entity: E) -> None: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...

    @abstractmethod
    async def count(self) -> int: ...