import json
import yaml
from typer.testing import CliRunner
from frictionless import program, extract, Detector, helpers

runner = CliRunner()
IS_UNIX = not helpers.is_platform("windows")


# General


def test_program_extract():
    result = runner.invoke(program, "extract data/table.csv")
    assert result.exit_code == 0
    assert result.stdout.count("table.csv")
    assert result.stdout.count("id  name")
    assert result.stdout.count("1  english")
    assert result.stdout.count("2  中国人")


def test_program_extract_header_rows():
    result = runner.invoke(program, "extract data/table.csv --json --header-rows '1,2'")
    assert result.exit_code == 0
    assert json.loads(result.stdout) == extract(
        "data/table.csv", layout={"headerRows": [1, 2]}
    )


def test_program_extract_header_join():
    result = runner.invoke(
        program, "extract data/table.csv --json --header-rows '1,2' --header-join ':'"
    )
    assert result.exit_code == 0
    assert json.loads(result.stdout) == extract(
        "data/table.csv", layout={"headerRows": [1, 2], "headerJoin": ":"}
    )


def test_program_extract_pick_fields():
    result = runner.invoke(program, "extract data/table.csv --json --pick-fields 'id'")
    assert result.exit_code == 0
    assert json.loads(result.stdout) == extract(
        "data/table.csv", layout={"pickFields": ["id"]}
    )


def test_program_extract_skip_fields():
    result = runner.invoke(program, "extract data/table.csv --json --skip-fields 'id'")
    assert result.exit_code == 0
    assert json.loads(result.stdout) == extract(
        "data/table.csv", layout={"skipFields": ["id"]}
    )


def test_program_extract_limit_fields():
    result = runner.invoke(program, "extract data/table.csv --json --limit-fields 1")
    assert result.exit_code == 0
    assert json.loads(result.stdout) == extract(
        "data/table.csv", layout={"limitFields": 1}
    )


def test_program_extract_offset_fields():
    result = runner.invoke(program, "extract data/table.csv --json --offset-fields 1")
    assert result.exit_code == 0
    assert json.loads(result.stdout) == extract(
        "data/table.csv", layout={"offsetFields": 1}
    )


def test_program_extract_pick_rows():
    result = runner.invoke(program, "extract data/table.csv --json --pick-rows 1")
    assert result.exit_code == 0
    assert json.loads(result.stdout) == extract(
        "data/table.csv", layout={"pickRows": [1]}
    )


def test_program_extract_skip_rows():
    result = runner.invoke(program, "extract data/table.csv --json --skip-rows 1")
    assert result.exit_code == 0
    assert json.loads(result.stdout) == extract(
        "data/table.csv", layout={"skipRows": [1]}
    )


def test_program_extract_limit_rows():
    result = runner.invoke(program, "extract data/table.csv --json --limit-rows 1")
    assert result.exit_code == 0
    assert json.loads(result.stdout) == extract("data/table.csv", layout={"limitRows": 1})


def test_program_extract_offset_rows():
    result = runner.invoke(program, "extract data/table.csv --json --offset-rows 1")
    assert result.exit_code == 0
    assert json.loads(result.stdout) == extract(
        "data/table.csv", layout={"offsetRows": 1}
    )


def test_program_extract_schema():
    result = runner.invoke(
        program, "extract data/table.csv --json --schema data/schema.json"
    )
    assert result.exit_code == 0
    assert json.loads(result.stdout) == extract(
        "data/table.csv", schema="data/schema.json"
    )


def test_program_extract_sync_schema():
    result = runner.invoke(
        program,
        "extract data/table.csv --json --schema data/schema-reverse.json --schema-sync",
    )
    assert result.exit_code == 0
    assert json.loads(result.stdout) == extract(
        "data/table.csv", schema="data/schema.json", detector=Detector(schema_sync=True)
    )


def test_program_extract_field_type():
    result = runner.invoke(program, "extract data/table.csv --json --field-type string")
    assert result.exit_code == 0
    assert json.loads(result.stdout) == extract(
        "data/table.csv", detector=Detector(field_type="string")
    )


def test_program_extract_field_names():
    result = runner.invoke(program, "extract data/table.csv --json --field-names 'a,b'")
    assert result.exit_code == 0
    assert json.loads(result.stdout) == extract(
        "data/table.csv", detector=Detector(field_names=["a", "b"])
    )


def test_program_extract_field_missing_values():
    result = runner.invoke(
        program, "extract data/table.csv --json --field-missing-values 1"
    )
    assert result.exit_code == 0
    assert json.loads(result.stdout) == extract(
        "data/table.csv", detector=Detector(field_missing_values=["1"])
    )


def test_program_extract_yaml():
    result = runner.invoke(program, "extract data/table.csv --json")
    assert result.exit_code == 0
    assert yaml.safe_load(result.stdout) == extract("data/table.csv")


def test_program_extract_json():
    result = runner.invoke(program, "extract data/table.csv --json")
    assert result.exit_code == 0
    assert json.loads(result.stdout) == extract("data/table.csv")


def test_program_extract_csv():
    result = runner.invoke(program, "extract data/table.csv --csv")
    assert result.exit_code == 0
    if IS_UNIX:
        with open("data/table.csv") as file:
            assert result.stdout == file.read()
