from __future__ import annotations
import json
from typing import TYPE_CHECKING, Optional, List, Dict
from datetime import datetime
from ...resource import Resource
from ...platform import platform
from ..interfaces import IRecord, IRecordItem, IQueryData
from ... import helpers
from .. import settings

if TYPE_CHECKING:
    from sqlalchemy import Table, MetaData
    from sqlalchemy.engine import Engine
    from ...formats.sql import SqlMapper


# TODO: move specific logic to endpoint classes
class Database:
    database_url: str
    engine: Engine
    mapper: SqlMapper
    metadata: MetaData
    project: Table
    records: Table

    def __init__(self, database_url: str):
        sa = platform.sqlalchemy
        sql = platform.frictionless_formats.sql
        self.database_url = database_url
        self.engine = sa.create_engine(self.database_url)
        self.mapper = sql.SqlMapper(self.engine.dialect.name)
        with self.engine.begin() as conn:
            self.metadata = sa.MetaData()
            self.metadata.reflect(conn, views=True)

            # Ensure project table
            project = self.metadata.tables.get(settings.PROJECT_IDENTIFIER)
            if project is None:
                project = sa.Table(
                    settings.PROJECT_IDENTIFIER,
                    self.metadata,
                    sa.Column("config", sa.Text),
                )
                self.metadata.create_all(conn, tables=[project])
            self.project = project

            # Ensure records table
            records = self.metadata.tables.get(settings.RECORDS_IDENTIFIER)
            if records is None:
                records = sa.Table(
                    settings.RECORDS_IDENTIFIER,
                    self.metadata,
                    sa.Column("path", sa.Text, primary_key=True),
                    sa.Column("type", sa.Text),
                    sa.Column("updated", sa.DateTime),
                    sa.Column("tableName", sa.Text, unique=True, nullable=True),
                    sa.Column("resource", sa.Text),
                    sa.Column("report", sa.Text),
                )
                self.metadata.create_all(conn, tables=[records])
            self.records = records

    # General

    def query(self, query: str) -> IQueryData:
        sa = platform.sqlalchemy
        with self.engine.begin() as conn:
            result = conn.execute(sa.text(query))
            header = list(result.keys())
            rows = [row.asdict() for row in result]
            return IQueryData(header=header, rows=rows)

    # Record

    # TODO: reuse insert code from SqlAdapter?
    def create_record(self, resource: Resource, *, on_progress=None) -> IRecord:
        sa = platform.sqlalchemy
        with resource, self.engine.begin() as conn:
            assert resource.path
            assert resource.name
            report = None
            table = None

            # Table
            if resource.type == "table":
                # Get table name
                found = False
                table_names = []
                table_name = resource.name
                template = f"{table_name}%s"
                items = self.list_records()
                for item in items:
                    table_names.append(item["tableName"])
                    if item["path"] == resource.path:
                        table_name = item["tableName"]
                        found = True
                if not found:
                    suffix = 1
                    while table_name in table_names:
                        table_name = template % suffix
                        suffix += 1

                # Remove existing table
                existing_table = self.metadata.tables.get(table_name)
                if existing_table is not None:
                    self.metadata.drop_all(conn, tables=[existing_table])

                # Create new table
                table = self.mapper.write_schema(
                    resource.schema,
                    table_name=table_name,  # type: ignore
                    with_metadata=True,
                )
                table.to_metadata(self.metadata)
                self.metadata.create_all(conn, tables=[table])

                # Write row
                def on_row(row):
                    buffer.append(self.mapper.write_row(row, with_metadata=True))
                    if len(buffer) > settings.BUFFER_SIZE:
                        conn.execute(sa.insert(table), buffer)
                        buffer.clear()
                    if on_progress:
                        on_progress(f"{resource.stats.rows} rows")

                # Validate/iterate
                buffer: List[Dict] = []
                report = resource.validate(on_row=on_row)
                if len(buffer):
                    conn.execute(sa.insert(table), buffer)

            # Other file types
            else:
                report = resource.validate()

            # Register resource
            conn.execute(
                sa.delete(self.records).where(self.records.c.path == resource.path)
            )
            conn.execute(
                sa.insert(self.records).values(
                    path=resource.path,
                    type=resource.datatype,
                    tableName=table.name if table is not None else None,
                    updated=datetime.now(),
                    resource=resource.to_json(),
                    report=report.to_json() if report is not None else "{}",
                )
            )

        # Return record
        record = self.select_record(resource.path)
        assert record
        return record

    def delete_record(self, path: str) -> Optional[IRecord]:
        sa = platform.sqlalchemy
        record = self.select_record(path)
        if record:
            with self.engine.begin() as conn:
                if record["tableName"]:
                    table = self.metadata.tables.get(record["tableName"])
                    if table is not None:
                        self.metadata.drop_all(conn, tables=[table])
                        self.metadata.remove(table)
                conn.execute(sa.delete(self.records).where(self.records.c.path == path))
            return record

    def list_records(self) -> List[IRecordItem]:
        sa = platform.sqlalchemy
        with self.engine.begin() as conn:
            result = conn.execute(
                sa.select(
                    self.records.c.path,
                    self.records.c.type,
                    self.records.c.updated,
                    self.records.c.tableName,
                    self.records.c.report,
                )
            )
            items: List[IRecordItem] = []
            for row in result:
                item = IRecordItem(
                    path=row.path,
                    type=row.type,
                    updated=row.updated.isoformat(),
                    tableName=row.tableName,
                )
                # https://github.com/frictionlessdata/application/issues/146
                if row.report:
                    report = json.loads(row.report)
                    if report:
                        item["errorCount"] = report["stats"]["errors"]
                items.append(item)
            return items

    def move_record(self, source: str, target: str) -> str:
        sa = platform.sqlalchemy
        with self.engine.begin() as conn:
            conn.execute(
                sa.update(self.records)
                .where(self.records.c.path == source)
                .values(path=target)
            )
            return target

    def select_record(self, path: str) -> Optional[IRecord]:
        sa = platform.sqlalchemy
        with self.engine.begin() as conn:
            row = conn.execute(
                sa.select(self.records).where(self.records.c.path == path)
            ).first()
            if row:
                return IRecord(
                    # TODO: why it's a type error here but not in other places
                    path=row.path,  # type: ignore
                    type=row.type,  # type: ignore
                    updated=row.updated.isoformat(),  # type: ignore
                    tableName=row.tableName,  # type: ignore
                    resource=json.loads(row.resource),  # type: ignore
                    report=json.loads(row.report),  # type: ignore
                )

    def update_record(self, path: str, *, resource: dict):
        sa = platform.sqlalchemy
        with self.engine.begin() as conn:
            conn.execute(
                sa.update(self.records)
                .where(self.records.c.path == path)
                .values(resource=helpers.to_json(resource))
            )
