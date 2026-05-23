from dataclasses import dataclass
from typing import Optional, List


@dataclass
class RoleFilterDTO:
    page: int = 1
    per_page: int = 20
    search: Optional[str] = None
    order_by: Optional[str] = None
    order_direction: str = "asc"
    include_deleted: bool = False
    values: Optional[List[str]] = None