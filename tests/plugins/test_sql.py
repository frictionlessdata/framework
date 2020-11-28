import os
import pytest
import datetime
import sqlalchemy as sa
from frictionless import Table, Package, Resource, FrictionlessException
from frictionless.plugins.sql import SqlDialect, SqlStorage
from dotenv import load_dotenv

load_dotenv(".env")


# Parser


def test_table_sql(database_url):
    dialect = SqlDialect(table="table")
    with Table(database_url, dialect=dialect) as table:
        assert table.schema == {
            "fields": [
                {"constraints": {"required": True}, "name": "id", "type": "integer"},
                {"name": "name", "type": "string"},
            ],
            "primaryKey": ["id"],
        }
        assert table.header == ["id", "name"]
        assert table.read_data() == [[1, "english"], [2, "中国人"]]


def test_table_sql_order_by(database_url):
    dialect = SqlDialect(table="table", order_by="id")
    with Table(database_url, dialect=dialect) as table:
        assert table.header == ["id", "name"]
        assert table.read_data() == [[1, "english"], [2, "中国人"]]


def test_table_sql_order_by_desc(database_url):
    dialect = SqlDialect(table="table", order_by="id desc")
    with Table(database_url, dialect=dialect) as table:
        assert table.header == ["id", "name"]
        assert table.read_data() == [[2, "中国人"], [1, "english"]]


def test_table_sql_table_is_required_error(database_url):
    table = Table(database_url)
    with pytest.raises(FrictionlessException) as excinfo:
        table.open()
    error = excinfo.value.error
    assert error.code == "dialect-error"
    assert error.note.count("'table' is a required property")


def test_table_sql_headers_false(database_url):
    dialect = SqlDialect(table="table")
    with Table(database_url, dialect=dialect, headers=False) as table:
        assert table.header == []
        assert table.read_data() == [["id", "name"], [1, "english"], [2, "中国人"]]


def test_table_sql_write(database_url):
    source = "data/table.csv"
    dialect = SqlDialect(table="name", order_by="id")
    with Table(source) as table:
        table.write(database_url, dialect=dialect)
    with Table(database_url, dialect=dialect) as table:
        assert table.header == ["id", "name"]
        assert table.read_data() == [[1, "english"], [2, "中国人"]]


# Storage


def test_storage_types(sqlite_url):
    engine = sa.create_engine(sqlite_url)
    prefix = "prefix_"

    # Export/Import
    source = Package("data/storage/types.json")
    storage = source.to_sql(engine=engine, prefix=prefix, force=True)
    target = Package.from_sql(engine=engine, prefix=prefix)

    # Assert metadata
    assert target.get_resource("types").schema == {
        "fields": [
            {"name": "any", "type": "string"},  # type fallback
            {"name": "array", "type": "string"},  # type fallback
            {"name": "boolean", "type": "boolean"},
            {"name": "date", "type": "date"},
            {"name": "date_year", "type": "date"},  # format removal
            {"name": "datetime", "type": "datetime"},
            {"name": "duration", "type": "string"},  # type fallback
            {"name": "geojson", "type": "string"},  # type fallback
            {"name": "geopoint", "type": "string"},  # type fallback
            {"name": "integer", "type": "integer"},
            {"name": "number", "type": "number"},
            {"name": "object", "type": "string"},  # type fallback
            {"name": "string", "type": "string"},
            {"name": "time", "type": "time"},
            {"name": "year", "type": "integer"},  # type downgrade
            {"name": "yearmonth", "type": "string"},  # type fallback
        ],
    }

    # Assert data
    assert target.get_resource("types").read_rows() == [
        {
            "any": "中国人",
            "array": '["Mike", "John"]',
            "boolean": True,
            "date": datetime.date(2015, 1, 1),
            "date_year": datetime.date(2015, 1, 1),
            "datetime": datetime.datetime(2015, 1, 1, 3, 0),
            "duration": "P1Y1M",
            "geojson": '{"type": "Point", "coordinates": [33, 33.33]}',
            "geopoint": "30,70",
            "integer": 1,
            "number": 7,
            "object": '{"chars": 560}',
            "string": "english",
            "time": datetime.time(3, 0),
            "year": 2015,
            "yearmonth": "2015-01",
        },
    ]

    # Cleanup storage
    storage.delete_package(target.resource_names)


def test_storage_integrity(sqlite_url):
    engine = sa.create_engine(sqlite_url)
    prefix = "prefix_"

    # Export/Import
    source = Package("data/storage/integrity.json")
    storage = source.to_sql(engine=engine, prefix=prefix, force=True)
    target = Package.from_sql(engine=engine, prefix=prefix)

    # Assert metadata (main)
    assert target.get_resource("integrity_main").schema == {
        "fields": [
            # added required
            {"name": "id", "type": "integer", "constraints": {"required": True}},
            {"name": "parent", "type": "integer"},
            {"name": "description", "type": "string"},
        ],
        "primaryKey": ["id"],
        "foreignKeys": [
            {"fields": ["parent"], "reference": {"resource": "", "fields": ["id"]}}
        ],
    }

    # Assert metadata (link)
    assert target.get_resource("integrity_link").schema == {
        "fields": [
            # added required
            {"name": "main_id", "type": "integer", "constraints": {"required": True}},
            # added required; removed unique
            {"name": "some_id", "type": "integer", "constraints": {"required": True}},
            # removed unique
            {"name": "description", "type": "string"},
        ],
        "primaryKey": ["main_id", "some_id"],
        "foreignKeys": [
            {
                "fields": ["main_id"],
                "reference": {"resource": "integrity_main", "fields": ["id"]},
            }
        ],
    }

    # Assert data (main)
    assert target.get_resource("integrity_main").read_rows() == [
        {"id": 1, "parent": None, "description": "english"},
        {"id": 2, "parent": 1, "description": "中国人"},
    ]

    # Assert data (link)
    assert target.get_resource("integrity_link").read_rows() == [
        {"main_id": 1, "some_id": 1, "description": "note1"},
        {"main_id": 2, "some_id": 2, "description": "note2"},
    ]

    # Cleanup storage
    storage.delete_package(target.resource_names)


def test_storage_constraints(sqlite_url):
    engine = sa.create_engine(sqlite_url)
    prefix = "prefix_"

    # Export/Import
    source = Package("data/storage/constraints.json")
    storage = source.to_sql(engine=engine, prefix=prefix, force=True)
    target = Package.from_sql(engine=engine, prefix=prefix)

    # Assert metadata
    assert target.get_resource("constraints").schema == {
        "fields": [
            {"name": "required", "type": "string", "constraints": {"required": True}},
            {"name": "minLength", "type": "string"},  # constraint removal
            {"name": "maxLength", "type": "string"},  # constraint removal
            {"name": "pattern", "type": "string"},  # constraint removal
            {"name": "enum", "type": "string"},  # constraint removal
            {"name": "minimum", "type": "integer"},  # constraint removal
            {"name": "maximum", "type": "integer"},  # constraint removal
        ],
    }

    # Assert data
    assert target.get_resource("constraints").read_rows() == [
        {
            "required": "passing",
            "minLength": "passing",
            "maxLength": "passing",
            "pattern": "passing",
            "enum": "passing",
            "minimum": 5,
            "maximum": 5,
        },
    ]

    # Cleanup storage
    storage.delete_package(target.resource_names)


@pytest.mark.parametrize(
    "field_name, cell",
    [
        ("required", ""),
        ("minLength", "bad"),
        ("maxLength", "badbadbad"),
        ("pattern", "bad"),
        ("enum", "bad"),
        ("minimum", 3),
        ("maximum", 9),
    ],
)
def test_storage_constraints_not_valid_error(sqlite_url, field_name, cell):
    engine = sa.create_engine(sqlite_url)
    package = Package("data/storage/constraints.json")
    resource = package.get_resource("constraints")
    # We set an invalid cell to the data property
    for index, field in enumerate(resource.schema.fields):
        if field.name == field_name:
            resource.data[1][index] = cell
    # NOTE: should we wrap these exceptions?
    with pytest.raises(sa.exc.IntegrityError):
        resource.to_sql(engine=engine, force=True)


def test_storage_read_resource_not_existent_error(sqlite_url):
    engine = sa.create_engine(sqlite_url)
    storage = SqlStorage(engine=engine)
    with pytest.raises(FrictionlessException) as excinfo:
        storage.read_resource("bad")
    error = excinfo.value.error
    assert error.code == "storage-error"
    assert error.note.count("does not exist")


def test_storage_write_resource_existent_error(sqlite_url):
    engine = sa.create_engine(sqlite_url)
    resource = Resource(path="data/table.csv")
    storage = resource.to_sql(engine=engine)
    with pytest.raises(FrictionlessException) as excinfo:
        storage.write_resource(resource)
    error = excinfo.value.error
    assert error.code == "storage-error"
    assert error.note.count("already exists")
    # Cleanup storage
    storage.delete_package(list(storage))


def test_storage_delete_resource_not_existent_error(sqlite_url):
    engine = sa.create_engine(sqlite_url)
    storage = SqlStorage(engine=engine)
    with pytest.raises(FrictionlessException) as excinfo:
        storage.delete_resource("bad")
    error = excinfo.value.error
    assert error.code == "storage-error"
    assert error.note.count("does not exist")


def test_storage_views_support(sqlite_url):
    engine = sa.create_engine(sqlite_url)
    engine.execute("CREATE TABLE 'table' (id INTEGER PRIMARY KEY, name TEXT)")
    engine.execute("INSERT INTO 'table' VALUES (1, 'english'), (2, '中国人')")
    engine.execute("CREATE VIEW 'table_view' AS SELECT * FROM 'table'")
    storage = SqlStorage(engine=engine)
    resource = storage.read_resource("table_view")
    assert resource.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
        ]
    }
    assert resource.read_rows() == [
        {"id": 1, "name": "english"},
        {"id": 2, "name": "中国人"},
    ]


def test_storage_resource_url_argument(sqlite_url):
    source = Resource(path="data/table.csv")
    source.to_sql(url=sqlite_url)
    target = Resource.from_sql(name="table", url=sqlite_url)
    assert target.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
        ]
    }
    assert target.read_rows() == [
        {"id": 1, "name": "english"},
        {"id": 2, "name": "中国人"},
    ]


def test_storage_package_url_argument(sqlite_url):
    source = Package(resources=[Resource(path="data/table.csv")])
    source.to_sql(url=sqlite_url)
    target = Package.from_sql(url=sqlite_url)
    assert target.get_resource("table").schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
        ]
    }
    assert target.get_resource("table").read_rows() == [
        {"id": 1, "name": "english"},
        {"id": 2, "name": "中国人"},
    ]


# Storage (PostgreSQL)


@pytest.mark.ci
def test_postgresql_storage_types():
    engine = sa.create_engine(os.environ["POSTGRESQL_URL"])
    prefix = "prefix_"

    # Export/Import
    source = Package("data/storage/types.json")
    storage = source.to_sql(engine=engine, prefix=prefix, force=True)
    target = Package.from_sql(engine=engine, prefix=prefix)

    # Assert metadata
    assert target.get_resource("types").schema == {
        "fields": [
            {"name": "any", "type": "string"},  # type fallback
            {"name": "array", "type": "object"},  # type downgrade
            {"name": "boolean", "type": "boolean"},
            {"name": "date", "type": "date"},
            {"name": "date_year", "type": "date"},  # format removal
            {"name": "datetime", "type": "datetime"},
            {"name": "duration", "type": "string"},  # type fallback
            {"name": "geojson", "type": "object"},  # type downgrade
            {"name": "geopoint", "type": "string"},  # type fallback
            {"name": "integer", "type": "integer"},
            {"name": "number", "type": "number"},
            {"name": "object", "type": "object"},
            {"name": "string", "type": "string"},
            {"name": "time", "type": "time"},
            {"name": "year", "type": "integer"},  # type downgrade
            {"name": "yearmonth", "type": "string"},  # type fallback
        ],
    }

    # Assert data
    assert target.get_resource("types").read_rows() == [
        {
            "any": "中国人",
            "array": None,  # TODO: fix array
            "boolean": True,
            "date": datetime.date(2015, 1, 1),
            "date_year": datetime.date(2015, 1, 1),
            "datetime": datetime.datetime(2015, 1, 1, 3, 0),
            "duration": "P1Y1M",
            "geojson": {"type": "Point", "coordinates": [33, 33.33]},
            "geopoint": "30,70",
            "integer": 1,
            "number": 7,
            "object": {"chars": 560},
            "string": "english",
            "time": datetime.time(3, 0),
            "year": 2015,
            "yearmonth": "2015-01",
        },
    ]

    # Cleanup storage
    storage.delete_package(target.resource_names)


@pytest.mark.ci
def test_postgresql_storage_integrity():
    engine = sa.create_engine(os.environ["POSTGRESQL_URL"])
    prefix = "prefix_"

    # Export/Import
    source = Package("data/storage/integrity.json")
    storage = source.to_sql(engine=engine, prefix=prefix, force=True)
    target = Package.from_sql(engine=engine, prefix=prefix)

    # Assert metadata (main)
    assert target.get_resource("integrity_main").schema == {
        "fields": [
            # added required
            {"name": "id", "type": "integer", "constraints": {"required": True}},
            {"name": "parent", "type": "integer"},
            {"name": "description", "type": "string"},
        ],
        "primaryKey": ["id"],
        "foreignKeys": [
            {"fields": ["parent"], "reference": {"resource": "", "fields": ["id"]}}
        ],
    }

    # Assert metadata (link)
    assert target.get_resource("integrity_link").schema == {
        "fields": [
            # added required
            {"name": "main_id", "type": "integer", "constraints": {"required": True}},
            # added required; removed unique
            {"name": "some_id", "type": "integer", "constraints": {"required": True}},
            # removed unique
            {"name": "description", "type": "string"},
        ],
        "primaryKey": ["main_id", "some_id"],
        "foreignKeys": [
            {
                "fields": ["main_id"],
                "reference": {"resource": "integrity_main", "fields": ["id"]},
            }
        ],
    }

    # Assert data (main)
    assert target.get_resource("integrity_main").read_rows() == [
        {"id": 1, "parent": None, "description": "english"},
        {"id": 2, "parent": 1, "description": "中国人"},
    ]

    # Assert data (link)
    assert target.get_resource("integrity_link").read_rows() == [
        {"main_id": 1, "some_id": 1, "description": "note1"},
        {"main_id": 2, "some_id": 2, "description": "note2"},
    ]

    # Cleanup storage
    storage.delete_package(target.resource_names)


# TODO: recover enum support
@pytest.mark.ci
@pytest.mark.skip
def test_postgresql_storage_constraints(sqlite_url):
    engine = sa.create_engine(os.environ["POSTGRESQL_URL"])
    prefix = "prefix_"

    # Export/Import
    source = Package("data/storage/constraints.json")
    storage = source.to_sql(engine=engine, prefix=prefix, force=True)
    target = Package.from_sql(engine=engine, prefix=prefix)

    # Assert metadata
    assert target.get_resource("constraints").schema == {
        "fields": [
            {"name": "required", "type": "string", "constraints": {"required": True}},
            {"name": "minLength", "type": "string"},  # constraint removal
            {"name": "maxLength", "type": "string"},  # constraint removal
            {"name": "pattern", "type": "string"},  # constraint removal
            {"name": "enum", "type": "string"},  # constraint removal
            {"name": "minimum", "type": "integer"},  # constraint removal
            {"name": "maximum", "type": "integer"},  # constraint removal
        ],
    }

    # Assert data
    assert target.get_resource("constraints").read_rows() == [
        {
            "required": "passing",
            "minLength": "passing",
            "maxLength": "passing",
            "pattern": "passing",
            "enum": "passing",
            "minimum": 5,
            "maximum": 5,
        },
    ]

    # Cleanup storage
    storage.delete_package(target.resource_names)


@pytest.mark.ci
@pytest.mark.parametrize(
    "field_name, cell",
    [
        ("required", ""),
        ("minLength", "bad"),
        ("maxLength", "badbadbad"),
        ("pattern", "bad"),
        ("enum", "bad"),
        ("minimum", 3),
        ("maximum", 9),
    ],
)
def test_postgresql_storage_constraints_not_valid_error(sqlite_url, field_name, cell):
    engine = sa.create_engine(os.environ["POSTGRESQL_URL"])
    package = Package("data/storage/constraints.json")
    resource = package.get_resource("constraints")
    # We set an invalid cell to the data property
    for index, field in enumerate(resource.schema.fields):
        if field.name == field_name:
            resource.data[1][index] = cell
    with pytest.raises((sa.exc.IntegrityError, sa.exc.DataError)):
        resource.to_sql(engine=engine, force=True)


@pytest.mark.ci
def test_postgresql_storage_views_support():
    engine = sa.create_engine(os.environ["POSTGRESQL_URL"])
    engine.execute("DROP VIEW IF EXISTS data_view")
    engine.execute("DROP TABLE IF EXISTS data")
    engine.execute("CREATE TABLE data (id INTEGER PRIMARY KEY, name TEXT)")
    engine.execute("INSERT INTO data VALUES (1, 'english'), (2, '中国人')")
    engine.execute("CREATE VIEW data_view AS SELECT * FROM data")
    storage = SqlStorage(engine=engine)
    resource = storage.read_resource("data_view")
    assert resource.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
        ]
    }
    assert resource.read_rows() == [
        {"id": 1, "name": "english"},
        {"id": 2, "name": "中国人"},
    ]


# Storage (MySQL)


@pytest.mark.ci
def test_mysql_storage_types():
    engine = sa.create_engine(os.environ["MYSQL_URL"])
    prefix = "prefix_"

    # Export/Import
    source = Package("data/storage/types.json")
    storage = source.to_sql(engine=engine, prefix=prefix, force=True)
    target = Package.from_sql(engine=engine, prefix=prefix)

    # Assert metadata
    assert target.get_resource("types").schema == {
        "fields": [
            {"name": "any", "type": "string"},  # type fallback
            {"name": "array", "type": "string"},  # type fallback
            {"name": "boolean", "type": "integer"},  # type downgrade
            {"name": "date", "type": "date"},
            {"name": "date_year", "type": "date"},  # format removal
            {"name": "datetime", "type": "datetime"},
            {"name": "duration", "type": "string"},  # type fallback
            {"name": "geojson", "type": "string"},  # type fallback
            {"name": "geopoint", "type": "string"},  # type fallback
            {"name": "integer", "type": "integer"},
            {"name": "number", "type": "number"},
            {"name": "object", "type": "string"},  # type fallback
            {"name": "string", "type": "string"},
            {"name": "time", "type": "time"},
            {"name": "year", "type": "integer"},  # type downgrade
            {"name": "yearmonth", "type": "string"},  # type fallback
        ],
    }

    # Assert data
    assert target.get_resource("types").read_rows() == [
        {
            "any": "中国人",
            "array": '["Mike", "John"]',
            "boolean": True,
            "date": datetime.date(2015, 1, 1),
            "date_year": datetime.date(2015, 1, 1),
            "datetime": datetime.datetime(2015, 1, 1, 3, 0),
            "duration": "P1Y1M",
            "geojson": '{"type": "Point", "coordinates": [33, 33.33]}',
            "geopoint": "30,70",
            "integer": 1,
            "number": 7,
            "object": '{"chars": 560}',
            "string": "english",
            "time": datetime.time(3, 0),
            "year": 2015,
            "yearmonth": "2015-01",
        },
    ]

    # Cleanup storage
    storage.delete_package(target.resource_names)


# TODO: fix unique for MySQL
@pytest.mark.ci
@pytest.mark.skip
def test_mysql_storage_integrity():
    engine = sa.create_engine(os.environ["MYSQL_URL"])
    prefix = "prefix_"

    # Export/Import
    source = Package("data/storage/integrity.json")
    storage = source.to_sql(engine=engine, prefix=prefix, force=True)
    target = Package.from_sql(engine=engine, prefix=prefix)

    # Assert metadata (main)
    assert target.get_resource("integrity_main").schema == {
        "fields": [
            # added required
            {"name": "id", "type": "integer", "constraints": {"required": True}},
            {"name": "parent", "type": "integer"},
            {"name": "description", "type": "string"},
        ],
        "primaryKey": ["id"],
        "foreignKeys": [
            {"fields": ["parent"], "reference": {"resource": "", "fields": ["id"]}}
        ],
    }

    # Assert metadata (link)
    assert target.get_resource("integrity_link").schema == {
        "fields": [
            # added required
            {"name": "main_id", "type": "integer", "constraints": {"required": True}},
            # added required; removed unique
            {"name": "some_id", "type": "integer", "constraints": {"required": True}},
            # removed unique
            {"name": "description", "type": "string"},
        ],
        "primaryKey": ["main_id", "some_id"],
        "foreignKeys": [
            {
                "fields": ["main_id"],
                "reference": {"resource": "integrity_main", "fields": ["id"]},
            }
        ],
    }

    # Assert data (main)
    assert target.get_resource("main").read_rows() == [
        {"id": 1, "parent": None, "description": "english"},
        {"id": 2, "parent": 1, "description": "中国人"},
    ]

    # Assert data (link)
    assert target.get_resource("link").read_rows() == [
        {"main_id": 1, "some_id": 1, "description": "note1"},
        {"main_id": 2, "some_id": 2, "description": "note2"},
    ]

    # Cleanup storage
    storage.delete_package(target.resource_names)


# TODO: fix enum for MySQL
@pytest.mark.ci
@pytest.mark.skip
def test_mysql_storage_constraints():
    engine = sa.create_engine(os.environ["MYSQL_URL"])
    prefix = "prefix_"

    # Export/Import
    source = Package("data/storage/constraints.json")
    storage = source.to_sql(engine=engine, prefix=prefix, force=True)
    target = Package.from_sql(engine=engine, prefix=prefix)

    # Assert metadata
    assert target.get_resource("constraints").schema == {
        "fields": [
            {"name": "required", "type": "string", "constraints": {"required": True}},
            {"name": "minLength", "type": "string"},  # constraint removal
            {"name": "maxLength", "type": "string"},  # constraint removal
            {"name": "pattern", "type": "string"},  # constraint removal
            {"name": "enum", "type": "string"},  # constraint removal
            {"name": "minimum", "type": "integer"},  # constraint removal
            {"name": "maximum", "type": "integer"},  # constraint removal
        ],
    }

    # Assert data
    assert target.get_resource("constraints").read_rows() == [
        {
            "required": "passing",
            "minLength": "passing",
            "maxLength": "passing",
            "pattern": "passing",
            "enum": "passing",
            "minimum": 5,
            "maximum": 5,
        },
    ]

    # Cleanup storage
    storage.delete_package(target.resource_names)


# TODO: fix consratins for MySQL
@pytest.mark.ci
@pytest.mark.skip
@pytest.mark.parametrize(
    "field_name, cell",
    [
        ("required", ""),
        ("minLength", "bad"),
        ("maxLength", "badbadbad"),
        ("pattern", "bad"),
        ("enum", "bad"),
        ("minimum", 3),
        ("maximum", 9),
    ],
)
def test_mysql_storage_constraints_not_valid_error(field_name, cell):
    engine = sa.create_engine(os.environ["MYSQL_URL"])
    package = Package("data/storage/constraints.json")
    resource = package.get_resource("constraints")
    # We set an invalid cell to the data property
    for index, field in enumerate(resource.schema.fields):
        if field.name == field_name:
            resource.data[1][index] = cell
    # NOTE: should we wrap these exceptions?
    with pytest.raises(sa.exc.IntegrityError):
        resource.to_sql(engine=engine, force=True)


@pytest.mark.ci
def test_mysql_storage_views_support():
    engine = sa.create_engine(os.environ["MYSQL_URL"])
    engine.execute("DROP VIEW IF EXISTS data_view")
    engine.execute("DROP TABLE IF EXISTS data")
    engine.execute("CREATE TABLE data (id INTEGER PRIMARY KEY, name TEXT)")
    engine.execute("INSERT INTO data VALUES (1, 'english'), (2, '中国人')")
    engine.execute("CREATE VIEW data_view AS SELECT * FROM data")
    storage = SqlStorage(engine=engine)
    resource = storage.read_resource("data_view")
    assert resource.schema == {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
        ]
    }
    assert resource.read_rows() == [
        {"id": 1, "name": "english"},
        {"id": 2, "name": "中国人"},
    ]
