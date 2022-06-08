from frictionless import Resource, Pipeline, steps


# General


def test_step_row_search():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.row_search(regex=r"^f.*"),
        ],
    )
    target = source.transform(pipeline)
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 2, "name": "france", "population": 66},
    ]


def test_step_row_search_with_name():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.row_search(regex=r"^f.*", field_name="name"),
        ],
    )
    target = source.transform(pipeline)
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 2, "name": "france", "population": 66},
    ]


def test_step_row_search_with_negate():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.row_search(regex=r"^f.*", negate=True),
        ],
    )
    target = source.transform(pipeline)
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83},
        {"id": 3, "name": "spain", "population": 47},
    ]
