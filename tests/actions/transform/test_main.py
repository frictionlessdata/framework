from frictionless import Resource, Step, transform, steps


# General


def test_transform():
    target = transform(
        "data/transform.csv",
        steps=[
            steps.table_normalize(),
            steps.table_melt(field_name="id"),
        ],
    )
    assert isinstance(target, Resource)
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "variable"},
            {"name": "value"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "variable": "name", "value": "germany"},
        {"id": 1, "variable": "population", "value": 83},
        {"id": 2, "variable": "name", "value": "france"},
        {"id": 2, "variable": "population", "value": 66},
        {"id": 3, "variable": "name", "value": "spain"},
        {"id": 3, "variable": "population", "value": 47},
    ]


def test_transform_custom_step_function_based():

    # Create step
    def custom(resource: Resource):
        current = resource.to_copy()

        # Data
        def data():
            with current:
                for row in current.row_stream:  # type: ignore
                    row["id"] = row["id"] * row["id"]
                    yield row

        # Meta
        resource.data = data

    # Transform resource
    # TODO: add typing support for function-based steps
    target = transform("data/transform.csv", steps=[Step(function=custom)])  # type: ignore
    assert isinstance(target, Resource)
    assert target.schema == {
        "fields": [
            {"type": "integer", "name": "id"},
            {"type": "string", "name": "name"},
            {"type": "integer", "name": "population"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83},
        {"id": 4, "name": "france", "population": 66},
        {"id": 9, "name": "spain", "population": 47},
    ]
