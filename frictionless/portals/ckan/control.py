from __future__ import annotations
import attrs
from typing import Optional, List
from ...dialect import Control


@attrs.define(kw_only=True)
class CkanControl(Control):
    """Ckan control representation"""

    type = "ckan"

    # State

    baseurl: Optional[str] = None
    """TODO: add docs"""

    dataset: Optional[str] = None
    """TODO: add docs"""

    resource: Optional[str] = None
    """TODO: add docs"""

    apikey: Optional[str] = None
    """TODO: add docs"""

    fields: Optional[List[str]] = None
    """TODO: add docs"""

    limit: Optional[int] = None
    """TODO: add docs"""

    sort: Optional[str] = None
    """TODO: add docs"""

    filters: Optional[dict] = None
    """TODO: add docs"""

    # Metadata

    metadata_profile_patch = {
        "properties": {
            "baseurl": {"type": "string"},
            "dataset": {"type": "string"},
            "resource": {"type": "string"},
            "apikey": {"type": "string"},
            "fields": {"type": "array", "items": {"type": "string"}},
            "limit": {"type": "integer"},
            "sort": {"type": "string"},
            "filters": {"type": "object"},
        },
    }