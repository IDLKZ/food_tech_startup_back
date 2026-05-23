import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('APP_ENV', 'dev')}",
        env_file_encoding="utf-8",
        extra="ignore",
    )