from __future__ import annotations
import attrs
from typing import Union
from ...dialect import Control
from . import settings


@attrs.define(kw_only=True)
class OdsControl(Control):
    """Ods control representation"""

    type = "ods"

    # State

    sheet: Union[str, int] = settings.DEFAULT_SHEET
    """TODO: add docs"""

    # Metadata

    metadata_profile = Control.metadata_merge(
        {
            "properties": {
                "sheet": {"type": ["number", "string"]},
            },
        }
    )
