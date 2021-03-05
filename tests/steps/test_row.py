from frictionless import Resource, transform, steps


# Filter


def test_step_row_filter():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(formula="id > 1"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 2, "name": "france", "population": 66},
        {"id": 3, "name": "spain", "population": 47},
    ]


def test_step_row_filter_with_function():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(function=lambda row: row["id"] > 1),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 2, "name": "france", "population": 66},
        {"id": 3, "name": "spain", "population": 47},
    ]


def test_step_row_filter_petl_selectop():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(formula="id == 1"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83},
    ]


def test_step_row_filter_petl_selecteq():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(formula="id == 1"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83},
    ]


def test_step_row_filter_petl_selectne():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(formula="id != 1"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 2, "name": "france", "population": 66},
        {"id": 3, "name": "spain", "population": 47},
    ]


def test_step_row_filter_petl_selectlt():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(formula="id < 2"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83},
    ]


def test_step_row_filter_petl_selectle():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(formula="id <= 2"),
        ],
    )
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
    ]


def test_step_row_filter_petl_selectgt():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(formula="id > 2"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 3, "name": "spain", "population": 47},
    ]


def test_step_row_filter_petl_selectge():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(formula="id >= 2"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 2, "name": "france", "population": 66},
        {"id": 3, "name": "spain", "population": 47},
    ]


def test_step_row_filter_petl_selectrangeopen():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(formula="1 <= id <= 3"),
        ],
    )
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
    ]


def test_step_row_filter_petl_selectrangeopenleft():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(formula="1 <= id < 3"),
        ],
    )
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
    ]


def test_step_row_filter_petl_selectrangeopenright():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(formula="1 < id <= 3"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 2, "name": "france", "population": 66},
        {"id": 3, "name": "spain", "population": 47},
    ]


def test_step_row_filter_petl_selectrangeclosed():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(formula="1 < id < 3"),
        ],
    )
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


def test_step_row_filter_petl_selectcontains():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_filter(formula="'er' in name"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83},
    ]


def test_step_row_filter_petl_selectin():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(formula="id in [1]"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83},
    ]


def test_step_row_filter_petl_selectnoin():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(formula="id not in [2, 3]"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83},
    ]


def test_step_row_filter_petl_selectis():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(formula="id is 1"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83},
    ]


def test_step_row_filter_petl_selectisnot():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(formula="id is not 1"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 2, "name": "france", "population": 66},
        {"id": 3, "name": "spain", "population": 47},
    ]


def test_step_row_filter_petl_selectisinstance():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.table_normalize(),
            steps.row_filter(function=lambda row: isinstance(row["id"], int)),
        ],
    )
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
    ]


def test_step_row_filter_petl_selectistrue():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_filter(function=lambda row: bool(row["id"])),
        ],
    )
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
    ]


def test_step_row_filter_petl_selectisfalse():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_filter(function=lambda row: not bool(row["id"])),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == []


def test_step_row_filter_petl_selectnone():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_filter(formula="id is None"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == []


def test_step_row_filter_petl_selectisnone():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_filter(formula="id is not None"),
        ],
    )
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
    ]


def test_step_row_filter_petl_rowlenselect():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_filter(function=lambda row: len(row) == 3),
        ],
    )
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
    ]


# Search


def test_step_row_search():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_search(regex=r"^f.*"),
        ],
    )
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
    target = transform(
        source,
        steps=[
            steps.row_search(regex=r"^f.*", field_name="name"),
        ],
    )
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
    target = transform(
        source,
        steps=[
            steps.row_search(regex=r"^f.*", negate=True),
        ],
    )
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


# Slice


def test_step_row_slice():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_slice(stop=2),
        ],
    )
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
    ]


def test_step_row_slice_with_start():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_slice(start=1, stop=2),
        ],
    )
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


def test_step_row_slice_with_start_and_step():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_slice(start=1, stop=3, step=2),
        ],
    )
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


def test_step_row_slice_with_head():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_slice(head=2),
        ],
    )
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
    ]


def test_step_row_slice_with_tail():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_slice(tail=2),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 2, "name": "france", "population": 66},
        {"id": 3, "name": "spain", "population": 47},
    ]


# Sort


def test_step_row_sort():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_sort(field_names=["name"]),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 2, "name": "france", "population": 66},
        {"id": 1, "name": "germany", "population": 83},
        {"id": 3, "name": "spain", "population": 47},
    ]


def test_step_row_sort_with_reverse():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_sort(field_names=["id"], reverse=True),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 3, "name": "spain", "population": 47},
        {"id": 2, "name": "france", "population": 66},
        {"id": 1, "name": "germany", "population": 83},
    ]


# Split


def test_step_row_split():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_split(field_name="name", pattern="a"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germ", "population": 83},
        {"id": 1, "name": "ny", "population": 83},
        {"id": 2, "name": "fr", "population": 66},
        {"id": 2, "name": "nce", "population": 66},
        {"id": 3, "name": "sp", "population": 47},
        {"id": 3, "name": "in", "population": 47},
    ]


# Subset


def test_step_row_subset_conflicts():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_subset(subset="conflicts", field_name="id"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == []


def test_step_row_subset_conflicts_with_duplicates():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.field_update(name="id", value=1),
            steps.row_subset(subset="conflicts", field_name="id"),
        ],
    )
    assert target.schema == {
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
    target = transform(
        source,
        steps=[
            steps.row_subset(subset="distinct", field_name="id"),
        ],
    )
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
    ]


def test_step_row_subset_distinct_with_duplicates():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.field_update(name="id", value=1),
            steps.row_subset(subset="distinct", field_name="id"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "germany", "population": 83},
    ]


def test_step_row_subset_duplicates():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_subset(subset="duplicates"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == []


def test_step_row_subset_duplicates_with_name():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.field_update(name="id", value=1),
            steps.row_subset(subset="duplicates", field_name="id"),
        ],
    )
    assert target.schema == {
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


def test_step_row_subset_unique():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.row_subset(subset="unique"),
        ],
    )
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
    ]


def test_step_row_subset_unique_with_name():
    source = Resource("data/transform.csv")
    target = transform(
        source,
        steps=[
            steps.field_update(name="id", value=1),
            steps.row_subset(subset="unique", field_name="id"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
        ]
    }
    assert target.read_rows() == []


# Ungroup


def test_step_row_ungroup_first():
    source = Resource("data/transform-groups.csv")
    target = transform(
        source,
        steps=[
            steps.row_ungroup(group_name="name", selection="first"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
            {"name": "year", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 3, "name": "france", "population": 66, "year": 2020},
        {"id": 1, "name": "germany", "population": 83, "year": 2020},
        {"id": 5, "name": "spain", "population": 47, "year": 2020},
    ]


def test_step_row_ungroup_last():
    source = Resource("data/transform-groups.csv")
    target = transform(
        source,
        steps=[
            steps.row_ungroup(group_name="name", selection="last"),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
            {"name": "year", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 4, "name": "france", "population": 54, "year": 1920},
        {"id": 2, "name": "germany", "population": 77, "year": 1920},
        {"id": 6, "name": "spain", "population": 33, "year": 1920},
    ]


def test_step_row_ungroup_min():
    source = Resource("data/transform-groups.csv")
    target = transform(
        source,
        steps=[
            steps.row_ungroup(
                group_name="name", selection="min", value_name="population"
            ),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
            {"name": "year", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 4, "name": "france", "population": 54, "year": 1920},
        {"id": 2, "name": "germany", "population": 77, "year": 1920},
        {"id": 6, "name": "spain", "population": 33, "year": 1920},
    ]


def test_step_row_ungroup_max():
    source = Resource("data/transform-groups.csv")
    target = transform(
        source,
        steps=[
            steps.row_ungroup(
                group_name="name", selection="max", value_name="population"
            ),
        ],
    )
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
            {"name": "population", "type": "integer"},
            {"name": "year", "type": "integer"},
        ]
    }
    assert target.read_rows() == [
        {"id": 3, "name": "france", "population": 66, "year": 2020},
        {"id": 1, "name": "germany", "population": 83, "year": 2020},
        {"id": 5, "name": "spain", "population": 47, "year": 2020},
    ]
