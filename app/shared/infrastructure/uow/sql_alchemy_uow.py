from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.infrastructure.uow.abstract_uow import BaseUoW


#Единая атомарная транзакция в проекте для SQL Alchemy

class SqlAlchemyUoW(BaseUoW):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def __aenter__(self) -> "SqlAlchemyUoW":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            await self.rollback()
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()