from __future__ import annotations
import attrs
import subprocess
from functools import cached_property
from typing import TYPE_CHECKING, Optional, Type
from ...exception import FrictionlessException
from ...schema import Schema, Field
from ...platform import platform

if TYPE_CHECKING:
    from ..resource import Resource


BLOCK_SIZE = 8096


def index(
    self: Resource,
    database_url: str,
    *,
    table_name: str,
    fast: bool = False,
    qsv: Optional[str] = None,
):
    """Index resource into a database"""

    # Prepare url
    if "://" not in database_url:
        database_url = f"sqlite:///{database_url}"
    url = platform.sqlalchemy.engine.make_url(database_url)

    # Select indexer
    ActualIndexer: Optional[Type[Indexer]] = None
    if url.drivername.startswith("postgresql"):
        ActualIndexer = FastPostgresIndexer if fast else PostgresIndexer
    if url.drivername.startswith("sqlite"):
        ActualIndexer = FastSqliteIndexer if fast else SqliteIndexer
    if not ActualIndexer:
        raise FrictionlessException(f"not supported database: {url.drivername}")

    # Run indexer
    indexer = ActualIndexer(
        resource=self,
        database_url=database_url,
        table_name=table_name,
        qsv=qsv,
    )
    indexer.index()


# Internal


@attrs.define(kw_only=True)
class Indexer:

    # State

    resource: Resource
    database_url: str
    table_name: str
    qsv: Optional[str] = None

    # Props

    @cached_property
    def engine(self):
        return platform.sqlalchemy.create_engine(self.database_url)

    @cached_property
    def mapper(self):
        return platform.frictionless_formats.sql.SqlMapper(self.engine)

    @cached_property
    def table(self):
        return self.mapper.write_schema(self.resource.schema, table_name=self.table_name)

    # Methods

    def index(self):
        self.infer_metadata()
        with self.resource:
            self.write_metadata()
            self.write_data()

    def infer_metadata(self):
        # TODO: move to formats.qsv.QsvMapper?
        if self.qsv:
            PIPE = subprocess.PIPE
            command = [self.qsv, "stats", "--infer-dates", "--dates-whitelist", "all"]
            process = subprocess.Popen(command, stdout=PIPE, stdin=PIPE)
            with self.resource.open(as_file=True):
                while True:
                    chunk = self.resource.read_bytes(size=BLOCK_SIZE)
                    if not chunk:
                        break
                    process.stdin.write(chunk)  # type: ignore
                process.stdin.close()  # type: ignore
                result = process.stdout.read()  # type: ignore
                process.wait()
                schema = Schema()
                with platform.frictionless.Resource(result, format="csv") as info:
                    for row in info.row_stream:
                        type = "string"
                        if row["type"] == "Integer":
                            type = "integer"
                        elif row["type"] == "Float":
                            type = "number"
                        elif row["type"] == "DateTime":
                            type = "datetime"
                        elif row["type"] == "Date":
                            type = "date"
                        descriptor = {"name": row["field"], "type": type}
                        schema.add_field(Field.from_descriptor(descriptor))
                self.resource.schema = schema

    def write_metadata(self):
        sql = platform.sqlalchemy_schema
        self.engine.execute(str(sql.DropTable(self.table, bind=self.engine, if_exists=True)))  # type: ignore
        self.engine.execute(str(sql.CreateTable(self.table, bind=self.engine)))  # type: ignore

    def write_data(self):
        raise NotImplementedError()


class PostgresIndexer(Indexer):

    # Methods

    def write_data(self):
        with platform.psycopg.connect(self.database_url) as connection:
            with connection.cursor() as cursor:
                query = 'COPY "%s" FROM STDIN' % self.table_name
                with cursor.copy(query) as copy:  # type: ignore

                    # Write row
                    def callback(row):
                        cells = self.mapper.write_row(row)
                        copy.write_row(cells)

                    # Validate/iterate
                    self.resource.validate(callback=callback)


class FastPostgresIndexer(Indexer):

    # Methods

    def write_data(self):
        with platform.psycopg.connect(self.database_url) as connection:
            with connection.cursor() as cursor:
                query = 'COPY "%s" FROM STDIN CSV HEADER' % self.table_name
                with cursor.copy(query) as copy:  # type: ignore
                    while True:
                        chunk = self.resource.read_bytes(size=BLOCK_SIZE)
                        if not chunk:
                            break
                        copy.write(chunk)


class SqliteIndexer(Indexer):

    # Methods

    def write_data(self):
        buffer = []
        buffer_size = 1000

        # Write row
        def callback(row):
            cells = self.mapper.write_row(row)
            buffer.append(cells)
            if len(buffer) > buffer_size:
                self.engine.execute(self.table.insert().values(buffer))
                buffer.clear()

        # Validate/iterate
        self.resource.validate(callback=callback)
        if len(buffer):
            self.engine.execute(self.table.insert().values(buffer))


class FastSqliteIndexer(Indexer):

    # Methods

    def write_data(self):
        # --csv and --skip options for .import are available from sqlite3@3.32
        # https://github.com/simonw/sqlite-utils/issues/297#issuecomment-880256058
        url = platform.sqlalchemy.engine.make_url(self.database_url)
        sql_command = f".import '|cat -' {self.table_name}"
        command = ["sqlite3", "-csv", url.database, sql_command]
        process = subprocess.Popen(command, stdin=subprocess.PIPE)
        for line_number, line in enumerate(self.resource.byte_stream, start=1):
            if line_number > 1:
                process.stdin.write(line)  # type: ignore
        process.stdin.close()  # type: ignore
        process.wait()
