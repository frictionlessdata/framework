import pytest
from frictionless import Resource, Dialect, FrictionlessException, formats


BASEURL = "https://raw.githubusercontent.com/frictionlessdata/frictionless-py/master/%s"


# Read


def test_xls_parser():
    with Resource("data/table.xls") as table:
        assert table.header == ["id", "name"]
        assert table.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


@pytest.mark.vcr
def test_xls_parser_remote():
    with Resource(BASEURL % "data/table.xls") as resource:
        assert resource.header == ["id", "name"]
        assert resource.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


def test_xls_parser_sheet_by_index():
    source = "data/sheet2.xls"
    control = formats.ExcelControl(sheet=2)
    with Resource(source, control=control) as resource:
        assert resource.header == ["id", "name"]
        assert resource.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


def test_xls_parser_sheet_by_index_not_existent():
    source = "data/sheet2.xls"
    control = formats.ExcelControl(sheet=3)
    with pytest.raises(FrictionlessException) as excinfo:
        Resource(source, control=control).open()
    assert 'sheet "3"' in str(excinfo.value)


def test_xls_parser_sheet_by_name():
    source = "data/sheet2.xls"
    control = formats.ExcelControl(sheet="Sheet2")
    with Resource(source, control=control) as resource:
        assert resource.header == ["id", "name"]
        assert resource.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


def test_xls_parser_sheet_by_name_not_existent():
    source = "data/sheet2.xls"
    control = formats.ExcelControl(sheet="bad")
    with pytest.raises(FrictionlessException) as excinfo:
        Resource(source, control=control).open()
    assert 'sheet "bad"' in str(excinfo.value)


def test_xls_parser_merged_cells():
    source = "data/merged-cells.xls"
    dialect = Dialect(header=False)
    with Resource(source, dialect=dialect) as resource:
        assert resource.read_rows() == [
            {"field1": "data", "field2": None},
            {"field1": None, "field2": None},
            {"field1": None, "field2": None},
        ]


def test_xls_parser_merged_cells_fill():
    source = "data/merged-cells.xls"
    control = formats.ExcelControl(fill_merged_cells=True)
    dialect = Dialect(header=False, controls=[control])
    with Resource(source, dialect=dialect) as resource:
        assert resource.read_rows() == [
            {"field1": "data", "field2": "data"},
            {"field1": "data", "field2": "data"},
            {"field1": "data", "field2": "data"},
        ]


def test_xls_parser_with_boolean():
    with Resource("data/table-with-booleans.xls") as resource:
        assert resource.header == ["id", "boolean"]
        assert resource.read_rows() == [
            {"id": 1, "boolean": True},
            {"id": 2, "boolean": False},
        ]


# Write


def test_xls_parser_write(tmpdir):
    source = Resource("data/table.csv")
    target = Resource(str(tmpdir.join("table.xls")))
    source.write(target)
    with target:
        assert target.header == ["id", "name"]
        assert target.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


def test_xls_parser_write_sheet_name(tmpdir):
    control = formats.ExcelControl(sheet="sheet")
    source = Resource("data/table.csv")
    target = Resource(str(tmpdir.join("table.xls")), control=control)
    source.write(target)
    with target:
        assert target.header == ["id", "name"]
        assert target.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


# Bugs


def test_xls_parser_cast_int_to_string_1251_xlsx():
    descriptor = {
        "name": "example",
        "type": "table",
        "path": "data/cast-int-to-string-issue-1251.xlsx",
        "scheme": "file",
        "format": "xlsx",
        "encoding": "utf-8",
        "mediatype": "application/vnd.ms-excel",
        "schema": {
            "fields": [
                {"name": "A", "type": "string"},
                {"name": "B", "type": "string"},
                {"name": "C", "type": "string"},
                {"name": "D", "type": "any"},
                {"name": "E", "type": "integer"},
            ]
        },
    }
    resource = Resource(descriptor, control=formats.ExcelControl(stringified=True))
    assert resource.read_rows() == [
        {"A": "001", "B": "b", "C": "1", "D": "a", "E": 1},
        {"A": "002", "B": "c", "C": "1", "D": "1", "E": 1},
    ]


def test_xls_parser_cast_int_to_string_1251_xls():
    descriptor = {
        "name": "example",
        "type": "table",
        "path": "data/cast-int-to-string-issue-1251.xlsx",
        "scheme": "file",
        "format": "xlsx",
        "encoding": "utf-8",
        "mediatype": "application/vnd.ms-excel",
        "schema": {
            "fields": [
                {"name": "A", "type": "string"},
                {"name": "B", "type": "string"},
                {"name": "C", "type": "string"},
                {"name": "D", "type": "any"},
                {"name": "E", "type": "integer"},
            ]
        },
    }
    resource = Resource(descriptor, control=formats.ExcelControl(stringified=True))
    assert resource.read_rows() == [
        {"A": "001", "B": "b", "C": "1", "D": "a", "E": 1},
        {"A": "002", "B": "c", "C": "1", "D": "1", "E": 1},
    ]
