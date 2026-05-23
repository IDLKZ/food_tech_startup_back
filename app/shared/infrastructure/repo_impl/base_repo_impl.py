from typing import Any, Generic, TypeVar, Optional
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import asc, desc, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from app.shared.infrastructure.dto.PaginationResult import PaginationResult
from app.shared.infrastructure.models.base_model import Base
from app.shared.infrastructure.filter.base_filter import BaseFilter

T = TypeVar("T", bound=Base)


class BaseRepoImpl(Generic[T]):

    def __init__(self, model: type[T], db: AsyncSession) -> None:
        self.model = model
        self.db = db

    # ── READ ──────────────────────────────────────────────────────

    async def get(
        self,
        id: UUID,
        options: list[Any] | None = None,
        include_deleted: bool = False,
    ) -> Optional[T]:
        filters = [self.model.id == id]
        filters = self._apply_soft_delete(filters, include_deleted)
        query = select(self.model).filter(*filters)
        if options:
            query = query.options(*options)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all(
        self,
        filters: list[Any] | None = None,
        options: list[Any] | None = None,
        order_by: str | None = None,
        order_direction: str = "asc",
        include_deleted: bool = False,
    ) -> list[T]:
        filters = self._apply_soft_delete(filters, include_deleted)
        query = select(self.model).filter(*filters)
        if options:
            query = query.options(*options)
        if order_by:
            query = self._apply_order_by(query, order_by, order_direction)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_first(
        self,
        filters: list[Any],
        options: list[Any] | None = None,
        order_by: str | None = None,
        order_direction: str = "asc",
        include_deleted: bool = False,
    ) -> Optional[T]:
        filters = self._apply_soft_delete(filters, include_deleted)
        query = select(self.model).filter(*filters)
        if options:
            query = query.options(*options)
        if order_by:
            query = self._apply_order_by(query, order_by, order_direction)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def paginate(
        self,
        page: int = 1,
        per_page: int = 20,
        filters: list[Any] | None = None,
        options: list[Any] | None = None,
        order_by: str | None = None,
        order_direction: str = "asc",
        include_deleted: bool = False,
    ) -> PaginationResult[T]:
        filters = self._apply_soft_delete(filters, include_deleted)
        query = select(self.model).filter(*filters)
        if options:
            query = query.options(*options)
        if order_by:
            query = self._apply_order_by(query, order_by, order_direction)

        total = await self.db.scalar(
            select(func.count()).select_from(query.subquery())
        ) or 0

        results = await self.db.execute(
            query.limit(per_page).offset((page - 1) * per_page)
        )
        return PaginationResult(
            items=list(results.scalars().all()),
            page=page,
            per_page=per_page,
            total_items=total,
            total_pages=(total + per_page - 1) // per_page,
        )

    async def paginate_with_filter(
        self,
        filter: BaseFilter,
        options: list[Any] | None = None,
    ) -> PaginationResult[T]:
        return await self.paginate(
            page=filter.page,
            per_page=filter.per_page,
            filters=filter.build(),
            options=options or self.default_relationships(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted=filter.include_deleted,
        )

    async def count(
        self,
        filters: list[Any] | None = None,
        include_deleted: bool = False,
    ) -> int:
        filters = self._apply_soft_delete(filters, include_deleted)
        query = select(func.count()).select_from(self.model).filter(*filters)
        result = await self.db.execute(query)
        return result.scalar() or 0

    # ── WRITE ─────────────────────────────────────────────────────

    async def save(self, obj: T) -> T:
        try:
            self.db.add(obj)
            await self.db.flush()
            return obj
        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError(self._parse_integrity_error(e))

    async def update(self, obj: T, data: dict) -> T:
        try:
            for field, value in data.items():
                if hasattr(obj, field):
                    setattr(obj, field, value)
            await self.db.flush()
            return obj
        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError(self._parse_integrity_error(e))

    async def delete(self, id: UUID, force: bool = False) -> bool:
        obj = await self.get(id, include_deleted=True)
        if not obj:
            return False
        if hasattr(obj, "deleted_at") and not force:
            obj.deleted_at = datetime.now(timezone.utc)
        else:
            await self.db.delete(obj)
        await self.db.flush()
        return True

    # ── HELPERS ───────────────────────────────────────────────────

    def _apply_soft_delete(
        self,
        filters: list[Any] | None,
        include_deleted: bool,
    ) -> list[Any]:
        filters = filters or []
        if not include_deleted and hasattr(self.model, "deleted_at"):
            filters.append(self.model.deleted_at.is_(None))
        return filters

    def _apply_order_by(self, query, order_by: str, order_direction: str):
        if order_direction.lower() == "desc":
            return query.order_by(desc(getattr(self.model, order_by)))
        return query.order_by(asc(getattr(self.model, order_by)))

    def _parse_integrity_error(self, error: IntegrityError) -> str:
        return f"IntegrityError: {str(error.orig).split(':')[-1].strip()}"

    def default_relationships(self) -> list[Any]:
        return []