from __future__ import annotations
from typing import TYPE_CHECKING
from ..report import Report
from .. import helpers

if TYPE_CHECKING:
    from .checklist import Checklist


# TODO: move exception handling to high-level actions?
@Report.from_validate
def validate(checklist: Checklist):
    """Validate checklist

    Returns:
        Report: validation report
    """
    timer = helpers.Timer()
    errors = checklist.metadata_errors
    return Report(errors=errors, time=timer.time)