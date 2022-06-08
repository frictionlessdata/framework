import pytest
from frictionless import Resource, Checklist, checks


# General


def test_validate_sequential_value():
    source = [
        ["row", "index2", "index3"],
        [2, 1, 1],
        [3, 2, 3],
        [4, 3, 5],
        [5, 5, 6],
        [6],
    ]
    resource = Resource(source)
    checklist = Checklist(
        checks=[
            checks.sequential_value(field_name="index2"),
            checks.sequential_value(field_name="index3"),
        ],
    )
    report = resource.validate(checklist)
    assert report.flatten(["rowPosition", "fieldPosition", "code"]) == [
        [3, 3, "sequential-value"],
        [5, 2, "sequential-value"],
        [6, 2, "missing-cell"],
        [6, 3, "missing-cell"],
    ]


@pytest.mark.skip
def test_validate_sequential_value_non_existent_field():
    source = [
        ["row", "name"],
        [2, "Alex"],
        [3, "Brad"],
    ]
    resource = Resource(source)
    checklist = Checklist(
        {
            "checks": [
                {"code": "sequential-value", "fieldName": "row"},
                {"code": "sequential-value", "fieldName": "bad"},
            ]
        }
    )
    report = resource.validate(checklist)
    assert report.flatten(["rowPosition", "fieldPosition", "code"]) == [
        [None, None, "check-error"],
    ]
