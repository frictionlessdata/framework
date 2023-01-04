import pytest
from frictionless import Field


# General


@pytest.mark.parametrize(
    "format, source, target",
    [
        ("default", "string", "string"),
        ("default", "", None),
        ("default", 0, None),
        ("uri", "http://google.com", "http://google.com"),
        ("uri", "://no-scheme.test", None),
        ("uri", "string", None),
        ("uri", "", None),
        ("uri", 0, None),
        ("email", "name@gmail.com", "name@gmail.com"),
        ("email", "http://google.com", None),
        ("email", "string", None),
        ("email", "", None),
        ("email", 0, None),
        ("binary", "dGVzdA==", "dGVzdA=="),
        ("binary", "", None),
        ("binary", "string", None),
        ("binary", 0, None),
        ("wkt", "POINT (30 10)", "POINT (30 10)"),
        ("wkt", "LINESTRING (30 10, 10 30, 40 40)", "LINESTRING (30 10, 10 30, 40 40)"),
        (
            "wkt",
            "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
            "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
        ),
        ("wkt", "string", None),
        ("wkt", "", None),
        ("wkt", 0, None),
    ],
)
def test_string_read_cell(format, source, target):
    field = Field.from_descriptor({"name": "name", "type": "string", "format": format})
    cell, notes = field.read_cell(source)
    assert cell == target
