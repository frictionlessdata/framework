from __future__ import annotations
from typing import TYPE_CHECKING
from ...platform import platform

if TYPE_CHECKING:
    from ..resource import Resource
    from ...report import Report


def index(self: Resource, database_url: str, *, table_name: str) -> Report:
    """Index resource into a database"""
    with self, platform.psycopg.connect(database_url) as connection:
        engine = platform.sqlalchemy.create_engine(database_url)
        mapper = platform.frictionless_formats.sql.SqlMapper()
        sql = platform.sqlalchemy_schema

        # Write metadata
        table = mapper.from_schema(self.schema, engine=engine, table_name=table_name)
        with connection.cursor() as cursor:
            cursor.execute(str(sql.DropTable(table, bind=engine, if_exists=True)))
            cursor.execute(str(sql.CreateTable(table, bind=engine)))

        # Write data
        with connection.cursor() as cursor:
            with cursor.copy('COPY "%s" FROM STDIN' % table_name) as copy:

                # Write row
                def callback(row):
                    cells = mapper.from_row(row)
                    copy.write_row(cells)

                # Return report
                report = self.validate(callback=callback)
                return report
