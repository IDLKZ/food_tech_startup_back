from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any
from sqlalchemy import or_, inspect
from sqlalchemy.orm import InstrumentedAttribute

from app.shared.infrastructure.models.base_model import Base

T = TypeVar("T", bound=Base)


class BaseFilter(ABC, Generic[T]):
    def __init__(
        self,
        model: type[T],
        page: int = 1,
        per_page: int = 20,
        search: str | None = None,
        order_by: str | None = None,
        order_direction: str = "asc",
        include_deleted: bool = False,
    ) -> None:
        self.model = model
        self.page = page
        self.per_page = per_page
        self.search = search
        self.order_by = order_by
        self.order_direction = order_direction
        self.include_deleted = include_deleted

    @abstractmethod
    def get_search_fields(self) -> list[str]: ...

    @abstractmethod
    def apply(self) -> list[Any]: ...

    def build(self) -> list[Any]:
        filters = []
        if self.search:
            model_columns = {col.key for col in inspect(self.model).columns}
            valid_fields = [
                f for f in self.get_search_fields() if f in model_columns
            ]
            if valid_fields:
                filters.append(
                    or_(
                        *[
                            getattr(self.model, f).ilike(f"%{self.search}%")
                            for f in valid_fields
                        ]
                    )
                )
        filters.extend(self.apply())
        return filters

    def get_order_by_column(self) -> InstrumentedAttribute | None:
        if self.order_by and hasattr(self.model, self.order_by):
            return getattr(self.model, self.order_by)
        return None