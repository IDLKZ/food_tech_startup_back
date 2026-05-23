from typing import Annotated, Optional, List
from fastapi import Query


class QueryConstants:

    @staticmethod
    def Page(description: str = "Номер страницы") -> int:
        return Query(1, ge=1, description=description)

    @staticmethod
    def PerPage(description: str = "Элементов на странице") -> int:
        return Query(20, ge=1, le=100, description=description)

    @staticmethod
    def Search(description: str = "Поиск") -> Optional[str]:
        return Query(None, max_length=255, description=description)

    @staticmethod
    def SortField(description: str = "Поле сортировки") -> Optional[str]:
        return Query(None, description=description)

    @staticmethod
    def SortDirection(description: str = "Направление сортировки") -> str:
        return Query("asc", pattern="^(asc|desc)$", description=description)

    @staticmethod
    def OptionalBool(description: str = "") -> Optional[bool]:
        return Query(None, description=description)

    @staticmethod
    def OptionalInt(description: str = "") -> Optional[int]:
        return Query(None, description=description)

    @staticmethod
    def OptionalStr(description: str = "") -> Optional[str]:
        return Query(None, description=description)

    @staticmethod
    def RequiredBool(description: str = "") -> bool:
        return Query(False, description=description)

    @staticmethod
    def OptionalListStr(description: str = "") -> Optional[List[str]]:
        return Query(None, description=description)

    @staticmethod
    def OptionalListInt(description: str = "") -> Optional[List[int]]:
        return Query(None, description=description)