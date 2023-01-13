from __future__ import annotations
import subprocess
from typing import TYPE_CHECKING, Optional
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
    sa = platform.sqlalchemy

    # Prepare url
    if "://" not in database_url:
        database_url = f"sqlite:///{database_url}"
    url = sa.engine.make_url(database_url)

    # Infer schema (qsv)
    if qsv:
        command = [qsv, "stats", "--infer-dates", "--dates-whitelist", "all"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        with self.open(as_file=True):
            while True:
                chunk = self.read_bytes(size=BLOCK_SIZE)
                if not chunk:
                    break
                process.stdin.write(chunk)  # type: ignore
            process.stdin.close()  # type: ignore
            result = process.stdout.read()  # type: ignore
            process.wait()
            schema = Schema()
            with self.__class__(result, format="csv") as info:
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
            self.schema = schema

    # Postgresql
    if url.drivername.startswith("postgresql"):
        engine = sa.create_engine(database_url)
        with self, platform.psycopg.connect(database_url) as connection:
            engine = platform.sqlalchemy.create_engine(database_url)
            mapper = platform.frictionless_formats.sql.SqlMapper(engine)
            sql = platform.sqlalchemy_schema

            # Write metadata
            table = mapper.write_schema(self.schema, table_name=table_name)
            with connection.cursor() as cursor:
                cursor.execute(str(sql.DropTable(table, bind=engine, if_exists=True)))  # type: ignore
                cursor.execute(str(sql.CreateTable(table, bind=engine)))  # type: ignore

            # Write data (fast)
            # TODO: raise if header is not in the first row
            if fast:
                with connection.cursor() as cursor:
                    query = 'COPY "%s" FROM STDIN CSV HEADER' % table_name
                    with cursor.copy(query) as copy:  # type: ignore
                        while True:
                            chunk = self.read_bytes(size=BLOCK_SIZE)
                            if not chunk:
                                break
                            copy.write(chunk)

            # Write data (general)
            else:
                with connection.cursor() as cursor:
                    query = 'COPY "%s" FROM STDIN' % table_name
                    with cursor.copy(query) as copy:  # type: ignore

                        # Write row
                        def callback(row):
                            cells = mapper.write_row(row)
                            copy.write_row(cells)

                        # Validate/iterate
                        self.validate(callback=callback)

    # Sqlite
    elif url.drivername.startswith("sqlite"):
        engine = sa.create_engine(database_url)
        with self:
            mapper = platform.frictionless_formats.sql.SqlMapper(engine)
            sql = platform.sqlalchemy_schema

            # Write metadata
            table = mapper.write_schema(self.schema, table_name=table_name)
            engine.execute(str(sql.DropTable(table, bind=engine, if_exists=True)))  # type: ignore
            engine.execute(str(sql.CreateTable(table, bind=engine)))  # type: ignore

            # Write data (fast)
            # TODO: raise if header is not in the first row
            if fast:
                # --csv and --skip options for .import are from sqlite3@3.32
                # https://github.com/simonw/sqlite-utils/issues/297#issuecomment-880256058
                sql_command = f".import '|cat -' {table_name}"
                command = ["sqlite3", "-csv", url.database, sql_command]
                process = subprocess.Popen(command, stdin=subprocess.PIPE)
                for line_number, line in enumerate(self.byte_stream, start=1):
                    if line_number > 1:
                        process.stdin.write(line)  # type: ignore
                process.stdin.close()  # type: ignore
                process.wait()

            # Write data (general)
            else:
                buffer = []
                buffer_size = 1000

                def callback(row):
                    cells = mapper.write_row(row)
                    buffer.append(cells)
                    if len(buffer) > buffer_size:
                        # sqlalchemy conn.execute(table.insert(), buffer)
                        # syntax applies executemany DB API invocation.
                        engine.execute(table.insert().values(buffer))
                        buffer.clear()

                # Validate/iterate
                self.validate(callback=callback)

                if len(buffer):
                    engine.execute(table.insert().values(buffer))

    # Not supported
    else:
        raise FrictionlessException(f"not supported database: {url.drivername}")
