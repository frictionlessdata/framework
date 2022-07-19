from __future__ import annotations
import attrs
from typing import Optional
from ...dialect import Control


@attrs.define(kw_only=True)
class BigqueryControl(Control):
    """Bigquery control representation"""

    type = "bigquery"

    # State

    table: Optional[str] = None
    """TODO: add docs"""

    dataset: Optional[str] = None
    """TODO: add docs"""

    project: Optional[str] = None
    """TODO: add docs"""

    prefix: Optional[str] = ""
    """TODO: add docs"""

    # Metadata

    metadata_profile_patch = {
        "properties": {
            "table": {"type": "string"},
            "dataset": {"type": "string"},
            "project": {"type": "string"},
            "prefix": {"type": "string"},
        },
    }