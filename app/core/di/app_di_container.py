# app/core/container.py
from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config.app_config import get_settings

"""
Контейнер с зависимостями
"""
class Container(containers.DeclarativeContainer):
    # Для чтения данных с конфига
    settings = providers.Singleton(get_settings)
    #Движки для чтения и записи в базу (CQRS)
    #1. Запись
    write_engine = providers.Singleton(
        create_async_engine,
        url=settings.provided.db.write_url,
        pool_size=settings.provided.db.db_write_pool_size,
        max_overflow=settings.provided.db.db_write_pool_max_overflow,
        pool_pre_ping=settings.provided.db.db_write_pool_pre_ping,
        echo=settings.provided.db.db_write_pool_echo,
    )
    #2. Чтение
    read_engine = providers.Singleton(
        create_async_engine,
        url=settings.provided.db.read_url,
        pool_size=settings.provided.db.db_read_pool_size,
        max_overflow=settings.provided.db.db_read_pool_max_overflow,
        pool_pre_ping=settings.provided.db.db_read_pool_pre_ping,
        echo=settings.provided.db.db_read_pool_echo,
    )
    #3. Синхронный движок для Alembic
    sync_engine = providers.Singleton(
        create_engine,  # из sqlalchemy
        url=settings.provided.db.sync_url,
    )

    # Сессионные фактории
    #1. SessionFactory для записи
    write_session_factory = providers.Singleton(
        async_sessionmaker,
        write_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    #2. SessionFactory для чтения
    read_session_factory = providers.Singleton(
        async_sessionmaker,
        read_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )