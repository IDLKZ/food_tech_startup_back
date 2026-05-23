from typing import Optional, List
from fastapi import Query
from app.modules.iam.application.dtos.role_filter_dto import RoleFilterDTO
from app.shared.presentation.dto.query_constants import QueryConstants


class RoleQueryFilter:
    def __init__(
        self,
        page: int = QueryConstants.Page(),
        per_page: int = QueryConstants.PerPage(),
        search: Optional[str] = QueryConstants.Search("Поиск по названию и коду"),
        order_by: Optional[str] = QueryConstants.SortField(),
        order_direction: str = QueryConstants.SortDirection(),
        include_deleted: bool = QueryConstants.RequiredBool("Показывать удалённые"),
        values: List[str] | None = QueryConstants.OptionalListStr("Фильтр по значениям"),
    ) -> None:
        self.page = page
        self.per_page = per_page
        self.search = search
        self.order_by = order_by
        self.order_direction = order_direction
        self.include_deleted = include_deleted
        self.values = values

    def to_dto(self) -> RoleFilterDTO:
        return RoleFilterDTO(
            page=self.page,
            per_page=self.per_page,
            search=self.search,
            order_by=self.order_by,
            order_direction=self.order_direction,
            include_deleted=self.include_deleted,
            values=self.values,
        )