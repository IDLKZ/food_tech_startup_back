from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class BaseUoW(ABC):

    @abstractmethod
    async def __aenter__(self) -> "BaseUoW": ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...