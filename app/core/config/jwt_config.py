from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.config.base_config import BaseConfig


class JWTSettings(BaseConfig):
    secret: str = Field(alias="JWT_SECRET")
    algorithm: str = Field(alias="JWT_ALGORITHM", default="HS256")
    access_expire_minutes: int = Field(alias="JWT_ACCESS_EXPIRE_MINUTES", default=60)
    refresh_expire_days: int = Field(alias="JWT_REFRESH_EXPIRE_DAYS", default=30)