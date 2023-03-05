import sys
from typing import Optional, Any
from ..checklist import Checklist, Check
from ..detector import Detector
from ..platform import platform
from ..dialect import Dialect
from .. import helpers


# Source


def create_source(source: Any, *, path: Optional[str] = None) -> Any:
    # Support stdin
    if source is None and path is None:
        if not sys.stdin.isatty():
            return sys.stdin.buffer.read()

    # Normalize
    if isinstance(source, list) and len(source) == 1:
        return source[0]

    return source


# Dialect


def create_dialect(
    *,
    descriptor: Optional[str],
    header_rows: Optional[str],
    header_join: Optional[str],
    comment_char: Optional[str],
    comment_rows: Optional[str],
    sheet: Optional[str],
    table: Optional[str],
    keys: Optional[str],
    keyed: Optional[bool],
) -> Dialect:
    formats = platform.frictionless_formats

    # Dialect
    descriptor = helpers.parse_json_string(descriptor)
    dialect = Dialect.from_descriptor(descriptor) if descriptor else Dialect()

    # Header rows
    if header_rows is not None:
        dialect.header_rows = helpers.parse_csv_string_typed(header_rows, convert=int)

    # Header join
    if header_join is not None:
        dialect.header_join = header_join

    # Comment char
    if comment_char is not None:
        dialect.comment_char = comment_char

    # Comment rows
    if comment_rows is not None:
        dialect.comment_rows = helpers.parse_csv_string_typed(comment_rows, convert=int)

    # Controls
    if sheet is not None:
        dialect.controls.append(formats.ExcelControl(sheet=sheet))
    elif table is not None:
        dialect.controls.append(formats.SqlControl(table=table))
    elif keys is not None or keyed is not None:
        dialect.controls.append(
            formats.JsonControl.from_options(
                keys=helpers.parse_csv_string(keys),
                keyed=keyed,
            )
        )

    return dialect


# Detector


def create_detector(
    *,
    buffer_size: Optional[int],
    sample_size: Optional[int],
    field_type: Optional[str],
    field_names: Optional[str],
    field_confidence: Optional[float],
    field_float_numbers: Optional[bool],
    field_missing_values: Optional[str],
    schema_sync: Optional[bool],
) -> Detector:
    # Detector
    detector = Detector()

    # Buffer size
    if buffer_size is not None:
        detector.buffer_size = buffer_size

    # Sample size
    if sample_size is not None:
        detector.sample_size = sample_size

    # Field type
    if field_type is not None:
        detector.field_type = field_type

    # Field names
    if field_names is not None:
        detector.field_names = helpers.parse_csv_string_typed(field_names)

    # Field confidence
    if field_confidence is not None:
        detector.field_confidence = field_confidence

    # Field float numbers
    if field_float_numbers is not None:
        detector.field_float_numbers = field_float_numbers

    # Field missing values
    if field_missing_values is not None:
        detector.field_missing_values = helpers.parse_csv_string_typed(
            field_missing_values
        )

    # Schema sync
    if schema_sync is not None:
        detector.schema_sync = schema_sync

    return detector


# Checklist


def create_checklist(
    *,
    descriptor: Optional[str] = None,
    checks: Optional[str] = None,
    pick_errors: Optional[str] = None,
    skip_errors: Optional[str] = None,
):
    # Checklist
    descriptor = helpers.parse_json_string(descriptor)
    checklist = Checklist.from_descriptor(descriptor) if descriptor else Checklist()

    # Checks
    for check in helpers.parse_descriptors_string(checks) or []:
        checklist.add_check(Check.from_descriptor(check))

    # Pick errors
    if pick_errors is not None:
        checklist.pick_errors = helpers.parse_csv_string_typed(pick_errors)

    # Skip errors
    if skip_errors is not None:
        checklist.skip_errors = helpers.parse_csv_string_typed(skip_errors)

    return checklist
