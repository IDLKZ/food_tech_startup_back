from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.config.base_config import BaseConfig
from app.core.config.db_config import DatabaseSettings
from app.core.config.jwt_config import JWTSettings
from app.core.config.rabbit_mq_settings import RabbitMQSettings
from app.core.config.redis_config import RedisSettings


class AppConfig(BaseConfig):
    env: str = Field(alias="APP_ENV", default="dev")
    debug: bool = Field(alias="APP_DEBUG", default=True)
    secret_key: str = Field(alias="APP_SECRET_KEY")

    # Вложенные конфигурации
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    jwt: JWTSettings = Field(default_factory=JWTSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    rabbitmq: RabbitMQSettings = Field(default_factory=RabbitMQSettings)



@lru_cache
def get_settings() -> AppConfig:
    return AppConfig()