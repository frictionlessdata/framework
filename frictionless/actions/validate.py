from typing import Optional, List, Any, Union
from ..exception import FrictionlessException
from ..checklist import Checklist, Check
from ..resource import Resource
from ..report import Report
from .. import settings


def validate(
    source: Optional[Any] = None,
    *,
    name: Optional[str] = None,
    type: Optional[str] = None,
    # Checklist
    checklist: Optional[Union[Checklist, str]] = None,
    checks: List[Check] = [],
    pick_errors: List[str] = [],
    skip_errors: List[str] = [],
    # Validate
    limit_errors: int = settings.DEFAULT_LIMIT_ERRORS,
    limit_rows: Optional[int] = None,
    parallel: bool = False,
    # Deprecated
    resource_name: Optional[str] = None,
    **options,
):
    """Validate resource

    Parameters:
        source (dict|str): a data source
        type (str): source type - inquiry, package, resource, schema or table
        **options (dict): options for the underlaying function

    Returns:
        Report: validation report
    """
    name = name or resource_name

    # Create checklist
    if isinstance(checklist, str):
        checklist = Checklist.from_descriptor(checklist)
    elif not checklist:
        checklist = Checklist(
            checks=checks,
            pick_errors=pick_errors,
            skip_errors=skip_errors,
        )

    # Create resource
    try:
        resource = Resource(source, datatype=type or "", **options)
    except FrictionlessException as exception:
        errors = exception.reasons if exception.reasons else [exception.error]
        return Report.from_validation(errors=errors)

    # Validate resource
    return resource.validate(
        checklist,
        name=name,
        parallel=parallel,
        limit_rows=limit_rows,
        limit_errors=limit_errors,
    )
