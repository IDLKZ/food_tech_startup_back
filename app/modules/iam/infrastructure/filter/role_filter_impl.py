from typing import Any

from app.shared.infrastructure.filter.base_filter import BaseFilter
from app.shared.infrastructure.models.iam.role_model import RoleModel
from app.modules.iam.application.dtos.role_filter_dto import RoleFilterDTO


class RoleFilterImpl(BaseFilter[RoleModel]):
    def __init__(self, dto: RoleFilterDTO) -> None:
        super().__init__(
            model=RoleModel,
            page=dto.page,
            per_page=dto.per_page,
            search=dto.search,
            order_by=dto.order_by,
            order_direction=dto.order_direction,
            include_deleted=dto.include_deleted,
        )
        self.values = dto.values

    def get_search_fields(self) -> list[str]:
        return ["title_ru", "title_kk", "title_en", "value"]

    def apply(self) -> list[Any]:
        filters = []
        if self.values is not None and len(self.values) > 0:
            filters.append(RoleModel.value in self.values)
        return filters