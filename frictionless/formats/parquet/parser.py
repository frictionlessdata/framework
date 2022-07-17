from __future__ import annotations
from ...resource import Resource
from .control import ParquetControl
from ...resource import Parser
from ... import helpers


class ParquetParser(Parser):
    """JSONL parser implementation."""

    # TODO: review here and in pandas
    supported_types = [
        "string",
    ]

    # Read

    def read_cell_stream_create(self):
        parquet = helpers.import_from_extras("fastparquet", name="parquet")
        control = ParquetControl.from_dialect(self.resource.dialect)
        file = parquet.ParquetFile(self.resource.normpath)
        for group, df in enumerate(file.iter_row_groups(**control.to_python()), start=1):
            with Resource(data=df, format="pandas") as resource:
                for line, cells in enumerate(resource.cell_stream, start=1):
                    # Starting from second group we don't need a header row
                    if group != 1 and line == 1:
                        continue
                    yield cells

    # Write

    # TODO: implement
    def write_row_stream(self, source):
        pass
