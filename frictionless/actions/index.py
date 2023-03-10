from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Any, List
from ..resource import Resource

if TYPE_CHECKING:
    from ..formats.sql import IOnRow, IOnProgress


def index(
    source: Optional[Any] = None,
    *,
    name: Optional[str] = None,
    type: Optional[str] = None,
    # Index
    database_url: str,
    fast: bool = False,
    on_row: Optional[IOnRow] = None,
    on_progress: Optional[IOnProgress] = None,
    use_fallback: bool = False,
    qsv_path: Optional[str] = None,
    **options,
) -> List[str]:
    """Index data into a database"""

    # Index resource
    resource = Resource(source, name=name or "", datatype=type or "", **options)
    return resource.index(
        database_url,
        fast=fast,
        on_row=on_row,
        on_progress=on_progress,
        use_fallback=use_fallback,
        qsv_path=qsv_path,
    )
