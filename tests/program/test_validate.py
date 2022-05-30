import json
import yaml
import re
from typer.testing import CliRunner
from frictionless import Metadata, Detector, program, validate

runner = CliRunner()


# General


def test_program_validate():
    result = runner.invoke(program, "validate data/table.csv")
    assert result.exit_code == 0
    assert result.stdout.count("valid: data/table.csv")


def test_program_validate_invalid():
    result = runner.invoke(program, "validate data/invalid.csv")
    assert result.exit_code == 1
    assert result.stdout.count("invalid: data/invalid.csv")


def test_program_validate_header_rows():
    result = runner.invoke(program, "validate data/table.csv --json --header-rows '1,2'")
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", layout={"headerRows": [1, 2]})
    )


def test_program_validate_header_join():
    result = runner.invoke(
        program, "validate data/table.csv --json --header-rows '1,2' --header-join ':'"
    )
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", layout={"headerRows": [1, 2], "headerJoin": ":"})
    )


def test_program_validate_pick_fields():
    result = runner.invoke(program, "validate data/table.csv --json --pick-fields 'id'")
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", layout={"pickFields": ["id"]})
    )


def test_program_validate_skip_fields():
    result = runner.invoke(program, "validate data/table.csv --json --skip-fields 'id'")
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", layout={"skipFields": ["id"]})
    )


def test_program_validate_limit_fields():
    result = runner.invoke(program, "validate data/table.csv --json --limit-fields 1")
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", layout={"limitFields": 1})
    )


def test_program_validate_offset_fields():
    result = runner.invoke(program, "validate data/table.csv --json --offset-fields 1")
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", layout={"offsetFields": 1})
    )


def test_program_validate_pick_rows():
    result = runner.invoke(program, "validate data/table.csv --json --pick-rows 1")
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", layout={"pickRows": [1]})
    )


def test_program_validate_skip_rows():
    result = runner.invoke(program, "validate data/table.csv --json --skip-rows 1")
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", layout={"skipRows": [1]})
    )


def test_program_validate_limit_rows():
    result = runner.invoke(program, "validate data/table.csv --json --limit-rows 1")
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", layout={"limitRows": 1})
    )


def test_program_validate_offset_rows():
    result = runner.invoke(program, "validate data/table.csv --json --offset-rows 1")
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", layout={"offsetRows": 1})
    )


def test_program_validate_infer_type():
    result = runner.invoke(program, "validate data/table.csv --json --field-type string")
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", detector=Detector(field_type="string"))
    )


def test_program_validate_field_names():
    result = runner.invoke(program, "validate data/table.csv --json --field-names 'a,b'")
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", detector=Detector(field_names=["a", "b"]))
    )


def test_program_validate_field_missing_values():
    result = runner.invoke(
        program, "validate data/table.csv --json --field-missing-values 1"
    )
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", detector=Detector(field_missing_values=["1"]))
    )


def test_program_validate_chucksum_hash():
    result = runner.invoke(
        program,
        "validate data/table.csv --json --stats-hash 6c2c61dd9b0e9c6876139a449ed87933",
    )
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", stats={"hash": "6c2c61dd9b0e9c6876139a449ed87933"})
    )


def test_program_validate_chucksum_bytes():
    result = runner.invoke(
        program,
        "validate data/table.csv --json --stats-bytes 30",
    )
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", stats={"bytes": 30})
    )


def test_program_validate_chucksum_rows():
    result = runner.invoke(
        program,
        "validate data/table.csv --json --stats-rows 2",
    )
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", stats={"rows": 2})
    )


def test_program_validate_pick_errors():
    result = runner.invoke(
        program,
        "validate data/table.csv --json --pick-errors 'blank-row,extra-cell'",
    )
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", pick_errors=["blank-row", "extra-cell"])
    )


def test_program_validate_skip_errors():
    result = runner.invoke(
        program,
        "validate data/table.csv --json --skip-errors 'blank-row,extra-cell'",
    )
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", skip_errors=["blank-row", "extra-cell"])
    )


def test_program_validate_limit_errors():
    result = runner.invoke(
        program,
        "validate data/table.csv --json --limit-errors 1",
    )
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(
        validate("data/table.csv", limit_errors=1)
    )


def test_program_validate_yaml():
    result = runner.invoke(program, "validate data/table.csv --yaml")
    assert result.exit_code == 0
    assert no_time(yaml.safe_load(result.stdout)) == no_time(validate("data/table.csv"))


def test_program_validate_json():
    result = runner.invoke(program, "validate data/table.csv --json")
    assert result.exit_code == 0
    assert no_time(json.loads(result.stdout)) == no_time(validate("data/table.csv"))


def test_program_validate_error_not_found():
    result = runner.invoke(program, "validate data/bad.csv")
    assert result.exit_code == 1
    assert result.stdout.count("[Errno 2]") and result.stdout.count("data/bad.csv")


def test_program_validate_zipped_resources_979():
    result = runner.invoke(program, "validate data/zipped-resources/datapackage.json")
    output_file_path = "data/fixtures/cli/zipped-resources-979.txt"
    with open(output_file_path, encoding="utf-8") as file:
        expected = file.read()
    assert result.exit_code == 1
    assert result.stdout.count("valid: ogd10_energieforschungstatistik_ch.csv")
    assert result.stdout.count("valid: ogd10_catalogs.zip => finanzquellen.csv")
    assert result.stdout.count("invalid: ogd10_catalogs.zip => capital-invalid.csv")
    assert result.stdout.count("Schema is not valid")
    # remove timetaken floating point number which varies
    output = re.sub(r"(\d+)\.(.*)\d", "", result.stdout)
    assert output.strip() == expected.strip()


def test_program_validate_long_error_messages_976():
    result = runner.invoke(program, "validate data/datapackage.json --type resource")
    output_file_path = "data/fixtures/cli/long-error-messages-976.txt"
    with open(output_file_path, encoding="utf-8") as file:
        expected = file.read()
    output = re.sub(r"(\d+)\.(.*)\d", "", result.stdout)
    assert result.exit_code == 1
    assert output.strip() == expected.strip()


def test_program_validate_partial_validation_info_933():
    result = runner.invoke(program, "validate data/countries.csv --limit-errors 2")
    assert result.exit_code == 1
    assert result.stdout.count(
        "The document was partially validated because of one of the limits"
    )
    assert result.stdout.count("Rows Checked(Partial)")


def test_program_validate_summary_1094():
    result = runner.invoke(program, "validate data/datapackage.json --type resource")
    assert result.exit_code == 1
    assert result.stdout.count("Summary")
    assert result.stdout.count("File name")
    assert result.stdout.count("File size")
    assert result.stdout.count("Total Time Taken (sec)")


def test_program_validate_single_resource_221():
    result = runner.invoke(
        program, "validate data/datapackage.json --resource-name number-two"
    )
    output_file_path = "data/fixtures/cli/single-resource-221.txt"
    with open(output_file_path, encoding="utf-8") as file:
        expected = file.read()
    output = re.sub(r"(\d+)\.(.*)\d", "", result.stdout)
    assert result.exit_code == 0
    assert output.strip() == expected.strip()


def test_program_validate_single_invalid_resource_221():
    result = runner.invoke(
        program, "validate data/datapackage.json --resource-name number-twoo"
    )
    output_file_path = "data/fixtures/cli/single-resource-invalid-221.txt"
    with open(output_file_path, encoding="utf-8") as file:
        expected = file.read()
    assert result.exit_code == 1
    assert result.stdout.strip() == expected.strip()


# Helpers


def no_time(descriptor):
    if isinstance(descriptor, Metadata):
        descriptor = descriptor.to_dict()
    for task in descriptor.get("tasks", []):
        task.pop("time", None)
    descriptor.pop("time", None)
    return descriptor
