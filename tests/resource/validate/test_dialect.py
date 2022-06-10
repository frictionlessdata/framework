from frictionless import Resource, helpers


# General


def test_validate_dialect_delimiter():
    resource = Resource("data/delimiter.csv", dialect={"delimiter": ";"})
    report = resource.validate()
    assert report.valid
    assert report.task.stats["rows"] == 2
