import pytest
from frictionless import Resource, helpers


# General


def test_validate_encoding():
    resource = Resource("data/table.csv", encoding="utf-8")
    report = resource.validate()
    assert report.valid


@pytest.mark.skipif(helpers.is_platform("windows"), reason="Fix on Windows")
def test_validate_encoding_invalid():
    resource = Resource("data/latin1.csv", encoding="utf-8")
    report = resource.validate()
    assert not report.valid
    assert report.flatten(["code", "note"]) == [
        [
            "encoding-error",
            "'utf-8' codec can't decode byte 0xa9 in position 20: invalid start byte",
        ],
    ]
