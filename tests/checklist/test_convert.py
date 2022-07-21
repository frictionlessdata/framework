import json
from frictionless import Checklist, checks


# General


def test_checklist():
    checklist = Checklist(checks=[checks.ascii_value()], pick_errors=["type-error"])
    descriptor = checklist.to_descriptor()
    print(descriptor)
    assert descriptor == {
        "checks": [{"type": "ascii-value"}],
        "pickErrors": ["type-error"],
    }


# Yaml


def test_checklist_to_yaml():
    checklist = Checklist.from_descriptor("data/checklist.json")
    output_file_path = "data/fixtures/convert/checklist.yaml"
    with open(output_file_path) as file:
        assert checklist.to_yaml().strip() == file.read().strip()


# Json


def test_checklist_to_json():
    checklist = Checklist.from_descriptor("data/checklist.yaml")
    assert json.loads(checklist.to_json()) == {
        "checks": [
            {
                "type": "deviated-cell",
                "interval": 3,
                "ignoreFields": ["Latitudine", "Longitudine"],
            }
        ]
    }


# Markdown


def test_checklist_markdown():
    checklist = Checklist.from_descriptor("data/checklist.json")
    output_file_path = "data/fixtures/convert/checklist.md"
    with open(output_file_path) as file:
        assert checklist.to_markdown().strip() == file.read()
