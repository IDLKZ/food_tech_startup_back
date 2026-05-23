from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.modules.iam.domain.entities.role_entity import RoleEntity
from app.modules.iam.domain.value_objects.role_value import RoleValue
from app.shared.infrastructure.models.iam.role_model import RoleModel
from app.shared.infrastructure.repo_impl.base_repo_impl import BaseRepoImpl


class RoleRepository(BaseRepoImpl[RoleModel]):

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(RoleModel, db)

    def default_relationships(self) -> list[Any]:
        return [selectinload(RoleModel.permissions)]

    async def create_role(self, entity: RoleEntity) -> None:
        await self.save(self._to_model(entity))
    # специфика
    async def get_by_value(self, value: str) -> Optional[RoleEntity]:
        m = await self.get_first(
            filters=[RoleModel.value == value],
            options=self.default_relationships(),
        )
        return self._to_entity(m) if m else None

    def _to_entity(self, m: RoleModel) -> RoleEntity:
        return RoleEntity(
            id=m.id,
            title_ru=m.title_ru,
            title_kk=m.title_kk,
            title_en=m.title_en,
            description_ru=m.description_ru,
            description_kk=m.description_kk,
            description_en=m.description_en,
            value=RoleValue(m.value),
            permission_ids=[rp.permission_id for rp in m.permissions],
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
        )

    def _to_model(self, entity: RoleEntity) -> RoleModel:
        return RoleModel(
            id=entity.id,
            title_ru=entity.title_ru,
            title_kk=entity.title_kk,
            title_en=entity.title_en,
            description_ru=entity.description_ru,
            description_kk=entity.description_kk,
            description_en=entity.description_en,
            value=str(entity.value),
        )

    def _update_model(self, m: RoleModel, entity: RoleEntity) -> None:
        m.title_ru = entity.title_ru
        m.title_kk = entity.title_kk
        m.title_en = entity.title_en
        m.description_ru = entity.description_ru
        m.description_kk = entity.description_kk
        m.description_en = entity.description_en
        m.deleted_at = entity.deleted_at
