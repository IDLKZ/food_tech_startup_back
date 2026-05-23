from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.di.app_di_container import Container


async def get_write_session() -> AsyncGenerator[AsyncSession, None]:
    factory = Container.write_session_factory()
    async with factory() as session:
        yield session


async def get_read_session() -> AsyncGenerator[AsyncSession, None]:
    factory = Container.read_session_factory()
    async with factory() as session:
        yield session