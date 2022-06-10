from frictionless import Resource, helpers


# General


def test_validate_scheme():
    resource = Resource("data/table.csv", scheme="file")
    report = resource.validate()
    assert report.valid


def test_validate_scheme_invalid():
    resource = Resource("bad://data/table.csv")
    report = resource.validate()
    assert report.flatten(["code", "note"]) == [
        [
            "scheme-error",
            'scheme "bad" is not supported. Try installing "frictionless-bad"',
        ],
    ]
