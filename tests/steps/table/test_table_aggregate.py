from frictionless import Resource, transform, steps


# General


def test_step_table_aggregate():
    source = Resource("data/transform-groups.csv")
    target = source.transform(
        steps=[
            steps.table_normalize(),
            steps.table_aggregate(
                group_name="name", aggregation={"sum": ("population", sum)}
            ),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "name", "type": "string"},
            {"name": "sum"},
        ]
    }
    assert target.read_rows() == [
        {"name": "france", "sum": 120},
        {"name": "germany", "sum": 160},
        {"name": "spain", "sum": 80},
    ]


def test_step_table_aggregate_multiple():
    source = Resource("data/transform-groups.csv")
    target = source.transform(
        steps=[
            steps.table_normalize(),
            steps.table_aggregate(
                group_name="name",
                aggregation={
                    "sum": ("population", sum),
                    "min": ("population", min),
                    "max": ("population", max),
                },
            ),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "name", "type": "string"},
            {"name": "sum"},
            {"name": "min"},
            {"name": "max"},
        ]
    }
    assert target.read_rows() == [
        {"name": "france", "sum": 120, "min": 54, "max": 66},
        {"name": "germany", "sum": 160, "min": 77, "max": 83},
        {"name": "spain", "sum": 80, "min": 33, "max": 47},
    ]
