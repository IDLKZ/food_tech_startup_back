from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.config.base_config import BaseConfig


class DatabaseSettings(BaseConfig):
    write_url: str = Field(alias="DATABASE_WRITE_URL")
    db_write_pool_size:int = Field(alias="DATABASE_WRITE_POOL_SIZE")
    db_write_pool_max_overflow:int = Field(alias="DATABASE_WRITE_POOL_MAX_OVERFLOW")
    db_write_pool_pre_ping: bool = Field(alias="DATABASE_WRITE_POOL_PRE_PING")
    db_write_pool_echo: bool = Field(alias="DATABASE_WRITE_POOL_ECHO")

    read_url: str = Field(alias="DATABASE_READ_URL")
    db_read_pool_size: int = Field(alias="DATABASE_READ_POOL_SIZE")
    db_read_pool_max_overflow: int = Field(alias="DATABASE_READ_POOL_MAX_OVERFLOW")
    db_read_pool_pre_ping: bool = Field(alias="DATABASE_READ_POOL_PRE_PING")
    db_read_pool_echo: bool = Field(alias="DATABASE_READ_POOL_ECHO")

    sync_url: str = Field(alias="DATABASE_SYNC_URL")