import os
import pytest
import sqlite3
import sqlalchemy as sa
from pytest_cov.embed import cleanup_on_sigterm


# Cleanups


cleanup_on_sigterm()


# Fixtures


@pytest.fixture
def database_url(tmpdir):
    path = str(tmpdir.join("database.db"))
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE 'table' (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO 'table' VALUES (1, 'english'), (2, '中国人')")
    conn.commit()
    yield "sqlite:///%s" % path
    conn.close()


@pytest.fixture
def sqlite_url(tmpdir):
    path = str(tmpdir.join("database.db"))
    return "sqlite:///%s" % path


@pytest.fixture
def postgresql_url():
    yield os.environ["POSTGRESQL_URL"]
    engine = sa.create_engine(os.environ["POSTGRESQL_URL"])
    conn = engine.connect()
    meta = sa.MetaData(bind=conn)
    meta.reflect(views=True)
    for table in reversed(meta.sorted_tables):
        conn.execute(table.delete())
    conn.close()


@pytest.fixture
def mysql_url():
    yield os.environ["MYSQL_URL"]
    engine = sa.create_engine(os.environ["MYSQL_URL"])
    conn = engine.connect()
    meta = sa.MetaData(bind=conn)
    meta.reflect(views=True)
    for table in reversed(meta.sorted_tables):
        conn.execute(table.delete())
    conn.close()


# Settings


def pytest_addoption(parser):
    parser.addoption(
        "--ci",
        action="store_true",
        dest="ci",
        default=False,
        help="enable integrational tests",
    )


def pytest_configure(config):
    if not config.option.ci:
        expr = getattr(config.option, "markexpr")
        setattr(config.option, "markexpr", "{expr} and not ci" if expr else "not ci")
