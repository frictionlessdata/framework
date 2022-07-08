from dataclasses import dataclass
from ...dialect import Control
from . import settings


@dataclass
class HtmlControl(Control):
    """Html control representation"""

    code = "html"

    # State

    selector: str = settings.DEFAULT_SELECTOR
    """TODO: add docs"""

    # Metadata

    metadata_profile = {  # type: ignore
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "code": {},
            "selector": {"type": "string"},
        },
    }