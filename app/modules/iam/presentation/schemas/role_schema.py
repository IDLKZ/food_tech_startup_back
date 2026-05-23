# app/modules/iam/presentation/schemas/role_schema.py
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class CreateRoleSchema(BaseModel):
    title_ru: str = Field(min_length=1, max_length=250)
    title_kk: Optional[str] = Field(None, max_length=250)
    title_en: Optional[str] = Field(None, max_length=250)
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None
    value: str = Field(min_length=2, max_length=50)


class RoleResponseSchema(BaseModel):
    id: UUID
    title_ru: str
    title_kk: Optional[str]
    title_en: Optional[str]
    description_ru: Optional[str]
    description_kk: Optional[str]
    description_en: Optional[str]
    value: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}