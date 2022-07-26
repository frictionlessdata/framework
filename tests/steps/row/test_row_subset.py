import pytest
from frictionless import Resource, Pipeline, steps


# General


def test_step_row_subset_conflicts():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.row_subset(subset="conflicts", field_name="id"),
        ],
    )
    target = source.transform(pipeline)
    assert target.schema.to_descriptor() == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == []


@pytest.mark.xfail(reason="steps")
def test_step_row_subset_conflicts_with_duplicates():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.field_update(name="id", value=1),
            steps.row_subset(subset="conflicts", field_name="id"),
        ],
    )
    target = source.transform(pipeline)
    assert target.schema.to_descriptor() == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83},
        {"id": 1, "name": "france", "population": 66},
        {"id": 1, "name": "spain", "population": 47},
    ]


def test_step_row_subset_distinct():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.row_subset(subset="distinct", field_name="id"),
        ],
    )
    target = source.transform(pipeline)
    assert target.schema.to_descriptor() == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83},
        {"id": 2, "name": "france", "population": 66},
        {"id": 3, "name": "spain", "population": 47},
    ]


@pytest.mark.xfail(reason="steps")
def test_step_row_subset_distinct_with_duplicates():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.field_update(name="id", value=1),
            steps.row_subset(subset="distinct", field_name="id"),
        ],
    )
    target = source.transform(pipeline)
    assert target.schema.to_descriptor() == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83},
    ]


@pytest.mark.xfail(reason="steps")
def test_step_row_subset_duplicates():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.row_subset(subset="duplicates"),  # type: ignore
        ],
    )
    target = source.transform(pipeline)
    assert target.schema.to_descriptor() == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == []


@pytest.mark.xfail(reason="steps")
def test_step_row_subset_duplicates_with_name():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.field_update(name="id", value=1),
            steps.row_subset(subset="duplicates", field_name="id"),
        ],
    )
    target = source.transform(pipeline)
    assert target.schema.to_descriptor() == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83},
        {"id": 1, "name": "france", "population": 66},
        {"id": 1, "name": "spain", "population": 47},
    ]


@pytest.mark.xfail(reason="steps")
def test_step_row_subset_unique():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.row_subset(subset="unique"),  # type: ignore
        ],
    )
    target = source.transform(pipeline)
    assert target.schema.to_descriptor() == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83},
        {"id": 2, "name": "france", "population": 66},
        {"id": 3, "name": "spain", "population": 47},
    ]


@pytest.mark.xfail(reason="steps")
def test_step_row_subset_unique_with_name():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.field_update(name="id", value=1),
            steps.row_subset(subset="unique", field_name="id"),
        ],
    )
    target = source.transform(pipeline)
    assert target.schema.to_descriptor() == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == []


# Bugs


@pytest.mark.xfail(reason="steps")
def test_step_row_subset_conflicts_from_descriptor_issue_996():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.row_subset({"subset": "conflicts", "fieldName": "id"}),  # type: ignore
        ],
    )
    target = source.transform(pipeline)
    assert target.schema.to_descriptor() == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == []
