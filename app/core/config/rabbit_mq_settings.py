from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.config.base_config import BaseConfig


class RabbitMQSettings(BaseConfig):
    url: str = Field(alias="RABBITMQ_URL")
    broker_url: str = Field(alias="CELERY_BROKER_URL")
    result_backend: str = Field(alias="CELERY_RESULT_BACKEND")