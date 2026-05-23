from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.config.base_config import BaseConfig


class RedisSettings(BaseConfig):
    url: str = Field(alias="REDIS_URL")