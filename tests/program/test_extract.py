import pytest
import json
import yaml
from typer.testing import CliRunner
from frictionless import extract, formats, Detector, platform, Dialect
from frictionless.program import program


runner = CliRunner()


# General


def test_program_extract():
    actual = runner.invoke(program, "extract data/table.csv")
    assert actual.exit_code == 0
    assert actual.stdout.count("table.csv")
    assert actual.stdout.count("id  name")
    assert actual.stdout.count("1  english")
    assert actual.stdout.count("2  中国人")


def test_program_extract_header_rows():
    actual = runner.invoke(program, "extract data/table.csv --json --header-rows '1,2'")
    expect = extract("data/table.csv", dialect=Dialect(header_rows=[1, 2]))
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == expect


def test_program_extract_header_join():
    actual = runner.invoke(
        program,
        "extract data/table.csv --json --header-rows '1,2' --header-join ':'",
    )
    expect = extract(
        "data/table.csv",
        dialect=Dialect(header_rows=[1, 2], header_join=":"),
    )
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == expect


def test_program_extract_comment_rows():
    actual = runner.invoke(program, "extract data/table.csv --json --comment-rows 1")
    expect = extract("data/table.csv", dialect=Dialect(comment_rows=[1]))
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == expect


def test_program_extract_schema():
    actual = runner.invoke(
        program,
        "extract data/table.csv --json --schema data/schema.json",
    )
    expect = extract(
        "data/table.csv",
        schema="data/schema.json",
    )
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == expect


def test_program_extract_sync_schema():
    actual = runner.invoke(
        program,
        "extract data/table.csv --json --schema data/schema-reverse.json --schema-sync",
    )
    expect = extract(
        "data/table.csv",
        schema="data/schema.json",
        detector=Detector(schema_sync=True),
    )
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == expect


def test_program_extract_field_type():
    actual = runner.invoke(program, "extract data/table.csv --json --field-type string")
    expect = extract("data/table.csv", detector=Detector(field_type="string"))
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == expect


def test_program_extract_field_names():
    actual = runner.invoke(program, "extract data/table.csv --json --field-names 'a,b'")
    expect = extract("data/table.csv", detector=Detector(field_names=["a", "b"]))
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == expect


def test_program_extract_field_missing_values():
    actual = runner.invoke(
        program, "extract data/table.csv --json --field-missing-values 1"
    )
    expect = extract(
        "data/table.csv",
        detector=Detector(field_missing_values=["1"]),
    )
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == expect


def test_program_extract_yaml():
    actual = runner.invoke(program, "extract data/table.csv --json")
    expect = extract("data/table.csv")
    assert actual.exit_code == 0
    assert yaml.safe_load(actual.stdout) == expect


def test_program_extract_json():
    actual = runner.invoke(program, "extract data/table.csv --json")
    expect = extract("data/table.csv")
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == expect


@pytest.mark.skipif(platform.type == "windows", reason="Fix on Windows")
def test_program_extract_csv():
    actual = runner.invoke(program, "extract data/table.csv --csv")
    with open("data/table.csv") as file:
        expect = file.read()
    assert actual.exit_code == 0
    assert actual.stdout == expect


def test_program_extract_dialect_sheet_option():
    actual = runner.invoke(program, "extract data/sheet2.xls --sheet Sheet2 --json")
    expect = extract("data/sheet2.xls", control=formats.ExcelControl(sheet="Sheet2"))
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == expect


@pytest.mark.skipif(platform.type == "windows", reason="Fix on Windows")
def test_program_extract_dialect_table_option_sql(database_url):
    actual = runner.invoke(program, f"extract {database_url} --table fruits --json")
    expect = extract(database_url, control=formats.SqlControl(table="fruits"))
    assert json.loads(actual.stdout) == expect


def test_program_extract_dialect_keyed_option():
    path = "data/table.keyed.json"
    actual = runner.invoke(program, f"extract --path {path} --keyed --json")
    expect = extract(path=path, control=formats.JsonControl(keyed=True))
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == expect


def test_program_extract_dialect_keys_option():
    path = "data/table.keyed.json"
    actual = runner.invoke(program, f"extract --path {path} --keys 'name,id' --json")
    expect = extract(path=path, control=formats.JsonControl(keys=["name", "id"]))
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == expect


def test_program_extract_valid_rows():
    actual = runner.invoke(program, "extract data/countries.csv --valid --json")
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == [
        {"id": 1, "neighbor_id": "Ireland", "name": "Britain", "population": "67"},
        {"id": 3, "neighbor_id": "22", "name": "Germany", "population": "83"},
        {"id": 4, "neighbor_id": None, "name": "Italy", "population": "60"},
    ]


def test_program_extract_yaml_valid_rows():
    actual = runner.invoke(program, "extract data/countries.csv --valid --yaml")
    assert actual.exit_code == 0
    with open("data/fixtures/issue-1004/valid-countries.yaml", "r") as stream:
        expect = yaml.safe_load(stream)
    assert yaml.safe_load(actual.stdout) == expect


def test_program_extract_invalid_rows():
    actual = runner.invoke(program, "extract data/countries.csv --invalid --json")
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == [
        {"id": 2, "neighbor_id": "3", "name": "France", "population": "n/a"},
        {"id": 5, "neighbor_id": None, "name": None, "population": None},
    ]


def test_program_extract_valid_rows_with_no_valid_rows():
    actual = runner.invoke(program, "extract data/invalid.csv --valid")
    assert actual.exit_code == 0
    assert actual.stdout.count("data: data/invalid.csv")
    assert actual.stdout.count("No valid rows")


def test_program_extract_invalid_rows_with_no_invalid_rows():
    actual = runner.invoke(program, "extract data/capital-valid.csv --invalid")
    assert actual.exit_code == 0
    assert actual.stdout.count("data: data/capital-valid.csv")
    assert actual.stdout.count("No invalid rows")


def test_program_extract_valid_rows_from_datapackage_with_multiple_resources():
    actual = runner.invoke(program, "extract data/issue-1004.package.json --valid --json")
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == {
        "issue-1004-data1": [
            {"id": 1, "neighbor_id": "Ireland", "name": "Britain", "population": "67"},
            {"id": 3, "neighbor_id": "22", "name": "Germany", "population": "83"},
            {"id": 4, "neighbor_id": None, "name": "Italy", "population": "60"},
        ],
        "issue-1004-data2": [],
    }


def test_program_extract_invalid_rows_from_datapackage_with_multiple_resources():
    actual = runner.invoke(
        program, "extract data/issue-1004.package.json --invalid --json"
    )
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == {
        "issue-1004-data1": [
            {"id": 2, "neighbor_id": "3", "name": "France", "population": "n/a"},
            {"id": 5, "neighbor_id": None, "name": None, "population": None},
        ],
        "issue-1004-data2": [
            {"id": 1, "name": "english", "country": None, "city": None},
            {"id": 1, "name": "english", "country": None, "city": None},
            {"id": None, "name": None, "country": None, "city": None},
            {"id": 2, "name": "german", "country": 1, "city": 2},
        ],
    }


def test_program_extract_valid_rows_extract_dialect_sheet_option():
    actual = runner.invoke(
        program, "extract data/sheet2.xls --sheet Sheet2 --json --valid"
    )
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == [
        {"id": 1, "name": "english"},
        {"id": 2, "name": "中国人"},
    ]


def test_program_extract_invalid_rows_extract_dialect_sheet_option():
    actual = runner.invoke(
        program, "extract data/sheet2.xls --sheet Sheet2 --json --invalid"
    )
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == []


def test_program_extract_single_resource():
    actual = runner.invoke(
        program, "extract data/datapackage.json --resource-name number-two --json"
    )
    assert actual.exit_code == 0
    assert json.loads(actual.stdout) == [
        {"id": 1, "name": "中国人"},
        {"id": 2, "name": "english"},
    ]


def test_program_extract_single_invalid_resource():
    actual = runner.invoke(
        program, "extract data/datapackage.json --resource-name number-twoo"
    )
    assert actual.exit_code == 1
    assert actual.stdout.count(
        'The data package has an error: resource "number-twoo" does not exist'
    )


def test_program_extract_single_valid_resource_invalid_package():
    actual = runner.invoke(
        program, "extract data/datapackagees.json --resource-name number-two"
    )
    assert actual.exit_code == 1
    assert actual.stdout.count("No such file or directory: 'data/datapackagees.json'")


def test_program_extract_single_resource_yaml():
    actual = runner.invoke(
        program, "extract data/datapackage.json --resource-name number-two --yaml"
    )
    expect = extract("data/datapackage.json", resource_name="number-two")
    assert actual.exit_code == 0
    assert yaml.safe_load(actual.stdout) == expect


def test_program_extract_single_resource_csv():
    actual = runner.invoke(
        program, "extract data/datapackage.json --resource-name number-two --csv"
    )
    assert actual.exit_code == 0
    assert (
        json.dumps(actual.stdout, ensure_ascii=False)
        == '"id,name\\n1,中国人\\n2,english\\n"'
    )


# Bugs


def test_extract_resource_from_csv_semicolon_delimiter_issue_1009():
    actual = runner.invoke(program, "extract data/issue-1009-semicolon.csv --csv")
    assert actual.exit_code == 0
    assert (
        json.dumps(actual.stdout, ensure_ascii=False)
        == '"fieldNameA;fieldNameB\\n0123;c\\n"'
    )


def test_extract_resource_from_csv_comma_delimiter_issue_1009():
    actual = runner.invoke(program, "extract data/issue-1009-comma.csv --csv")
    assert actual.exit_code == 0
    assert (
        json.dumps(actual.stdout, ensure_ascii=False)
        == '"fieldNameA,fieldNameB\\n123,c\\n"'
    )


def test_extract_resource_from_csv_semicolon_delimiter_param_issue_1009():
    actual = runner.invoke(
        program,
        'extract data/issue-1009-semicolon.csv --dialect \'{"delimiter": ";"}\' --csv',
    )
    assert actual.exit_code == 0
    assert (
        json.dumps(actual.stdout, ensure_ascii=False)
        == '"fieldNameA;fieldNameB\\n123;c\\n"'
    )


def test_extract_resource_from_csv_comma_delimiter_param_issue_1009():
    actual = runner.invoke(
        program,
        'extract data/issue-1009-comma.csv --dialect \'{"delimiter": ","}\' --csv',
    )
    assert actual.exit_code == 0
    assert (
        json.dumps(actual.stdout, ensure_ascii=False)
        == '"fieldNameA,fieldNameB\\n123,c\\n"'
    )
