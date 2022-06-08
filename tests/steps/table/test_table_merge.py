from frictionless import Resource, Pipeline, steps


# General


def test_step_table_merge():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.table_merge(
                resource=Resource(data=[["id", "name", "note"], [4, "malta", "island"]])
            ),
        ],
    )
    target = source.transform(pipeline)
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
            {"name": "note", "type": "string"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83, "note": None},
        {"id": 2, "name": "france", "population": 66, "note": None},
        {"id": 3, "name": "spain", "population": 47, "note": None},
        {"id": 4, "name": "malta", "population": None, "note": "island"},
    ]


def test_step_table_merge_from_dict():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.table_merge(
                resource=dict(data=[["id", "name", "note"], [4, "malta", "island"]])
            ),
        ],
    )
    target = source.transform(pipeline)
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
            {"name": "note", "type": "string"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83, "note": None},
        {"id": 2, "name": "france", "population": 66, "note": None},
        {"id": 3, "name": "spain", "population": 47, "note": None},
        {"id": 4, "name": "malta", "population": None, "note": "island"},
    ]


def test_step_table_merge_with_field_names():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.table_merge(
                resource=Resource(data=[["id", "name", "note"], [4, "malta", "island"]]),
                field_names=["id", "name"],
            ),
        ],
    )
    target = source.transform(pipeline)
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany"},
        {"id": 2, "name": "france"},
        {"id": 3, "name": "spain"},
        {"id": 4, "name": "malta"},
    ]


def test_step_merge_ignore_fields():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.table_merge(
                resource=Resource(data=[["id2", "name2"], [4, "malta"]]),
                ignore_fields=True,
            ),
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
        {"id": 2, "name": "france", "population": 66},
        {"id": 3, "name": "spain", "population": 47},
        {"id": 4, "name": "malta", "population": None},
    ]


def test_step_table_merge_with_sort():
    source = Resource("data/transform.csv")
    pipeline = Pipeline(
        steps=[
            steps.table_merge(
                resource=Resource(data=[["id", "name", "population"], [4, "malta", 1]]),
                sort_by_field=["population"],
            ),
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
        {"id": 4, "name": "malta", "population": 1},
        {"id": 3, "name": "spain", "population": 47},
        {"id": 2, "name": "france", "population": 66},
        {"id": 1, "name": "germany", "population": 83},
    ]
