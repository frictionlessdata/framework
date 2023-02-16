from __future__ import annotations
import re
from typing import Optional, TYPE_CHECKING
from ...system import Adapter
from ...package import Package
from ...platform import platform
from ...resource import Resource
from .control import SqlControl
from .mapper import SqlMapper

if TYPE_CHECKING:
    from sqlalchemy import MetaData
    from sqlalchemy.engine import Engine
    from ...schema import Schema


class SqlAdapter(Adapter):
    """Read and write data from/to SQL database"""

    engine: Engine
    control: SqlControl
    mapper: SqlMapper
    metadata: MetaData

    def __init__(self, engine: Engine, *, control: Optional[SqlControl] = None):
        sa = platform.sqlalchemy
        self.engine = engine
        self.control = control or SqlControl()
        self.mapper = SqlMapper(self.engine.dialect.name)
        with self.engine.begin() as conn:
            # It will fail silently if this function already exists
            if self.engine.dialect.name.startswith("sqlite"):
                conn.connection.create_function("REGEXP", 2, regexp)  # type: ignore
            self.metadata = sa.MetaData(schema=self.control.namespace)
            self.metadata.reflect(conn, views=True)

    # Read

    def read_package(self) -> Package:
        package = Package(resources=[])
        for table in self.metadata.sorted_tables:
            name = str(table.name)
            control = SqlControl(table=name)
            path = self.engine.url.render_as_string(hide_password=False)
            schema = self.mapper.read_schema(table)
            resource = Resource(path, name=name, schema=schema, control=control)
            package.add_resource(resource)
        return package

    def read_schema(self, table_name: str):
        table = self.metadata.tables[table_name]
        return self.mapper.read_schema(table)

    def read_cell_stream(self, control):
        sa = platform.sqlalchemy
        table = self.metadata.tables[control.table]
        with self.engine.begin() as conn:
            # Streaming could be not working for some backends:
            # http://docs.sqlalchemy.org/en/latest/core/connections.html
            query = sa.select(table).execution_options(stream_results=True)
            if control.order_by:
                query = query.order_by(sa.text(control.order_by))
            if control.where:
                query = query.where(sa.text(control.where))
            result = conn.execute(query)
            yield list(result.keys())
            for item in result:
                cells = list(item)
                yield cells

    # Write

    def write_package(self, package: Package) -> bool:
        with self.engine.begin() as conn:
            tables = []
            for res in package.resources:
                assert res.name
                table = self.mapper.write_schema(res.schema, table_name=res.name)
                table = table.to_metadata(self.metadata)
                tables.append(table)
            self.metadata.create_all(conn, tables=tables)
        for table in self.metadata.sorted_tables:
            if package.has_resource(table.name):
                resource = package.get_resource(table.name)
                with resource:
                    self.write_row_stream(resource.row_stream, table_name=table.name)
        return bool(tables)

    def write_schema(self, schema: Schema, *, table_name: str):
        with self.engine.begin() as conn:
            table = self.mapper.write_schema(schema, table_name=table_name)
            table = table.to_metadata(self.metadata)
            self.metadata.create_all(conn, tables=[table])

    def write_row_stream(self, row_stream, *, table_name: str):
        sa = platform.sqlalchemy
        with self.engine.begin() as conn:
            table = self.metadata.tables[table_name]
            buffer = []
            buffer_size = 1000
            for row in row_stream:
                cells = self.mapper.write_row(row)
                buffer.append(cells)
                if len(buffer) > buffer_size:
                    # sqlalchemy conn.execute(table.insert(), buffer)
                    # syntax applies executemany DB API invocation.
                    conn.execute(sa.insert(table).values(buffer))
                    buffer = []
            if len(buffer):
                conn.execute(sa.insert(table).values(buffer))


# Internal


def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None
