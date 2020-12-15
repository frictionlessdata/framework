# TODO: review this dependency
from .plugins.json import JsonParser
from itertools import zip_longest
from decimal import Decimal
from .helpers import cached_property
from . import helpers
from . import errors


class Row2(dict):
    """Row representation

    API      | Usage
    -------- | --------
    Public   | `from frictionless import Table`

    This object is returned by `extract`, `table.read_rows`, and other functions.

    ```python
    rows = extract("data/table.csv")
    for row in rows:
        # work with the Row
    ```

    Parameters:
        cells (any[]): array of cells
        schema (Schema): table schema
        field_positions (int[]): table field positions
        row_position (int): row position from 1
        row_number (int): row number from 1

    """

    def __init__(
        self,
        cells,
        *,
        schema,
        field_map,
        field_positions,
        row_position,
        row_number,
    ):
        self.__cells = cells
        self.__schema = schema
        self.__field_map = field_map
        self.__field_positions = field_positions
        self.__row_position = row_position
        self.__row_number = row_number
        self.__blank_cells = {}
        self.__error_cells = {}
        self.__partial = True
        self.__errors = []

    def __missing__(self, key):
        if self.__partial:
            value = self.__process(key)
            self[key] = value
            return value
        raise KeyError(key)

    def __str__(self):
        if self.__partial:
            self.__process()
        return super().__str__()

    def __repr__(self):
        if self.__partial:
            self.__process()
        return super().__repr__()

    def __iter__(self):
        if self.__partial:
            self.__process()
        return super().__iter__()

    def __len__(self):
        if self.__partial:
            self.__process()
        return super().__len__()

    def __contains__(self, key):
        if self.__partial:
            self.__process()
        return super().__contains__(key)

    def __reversed__(self, key):
        if self.__partial:
            self.__process()
        return super().__reversed__(key)

    def keys(self):
        if self.__partial:
            self.__process()
        return super().keys()

    def values(self):
        if self.__partial:
            self.__process()
        return super().values()

    def items(self):
        if self.__partial:
            self.__process()
        return super().items()

    @cached_property
    def blank_cells(self):
        """A mapping indexed by a field name with blank cells before parsing

        Returns:
            dict: row blank cells
        """
        if self.__partial:
            self.__process()
        return self.__blank_cells

    @cached_property
    def error_cells(self):
        """A mapping indexed by a field name with error cells before parsing

        Returns:
            dict: row error cells
        """
        if self.__partial:
            self.__process()
        return self.__error_cells

    @cached_property
    def errors(self):
        """
        Returns:
            Error[]: row errors
        """
        if self.__partial:
            self.__process()
        return self.__errors

    @cached_property
    def valid(self):
        """
        Returns:
            bool: if row valid
        """
        if self.__partial:
            self.__process()
        return not self.__errors

    @cached_property
    def cells(self):
        """
        Returns:
            any[]: original row cells
        """
        return self.__cells

    @cached_property
    def schema(self):
        """
        Returns:
            Schema: table schema
        """
        return self.__schema

    @cached_property
    def field_positions(self):
        """
        Returns:
            int[]: table field positions
        """
        return self.__field_positions

    @cached_property
    def row_position(self):
        """
        Returns:
            int: row position from 1
        """
        return self.__row_position

    @cached_property
    def row_number(self):
        """
        Returns:
            int: row number from 1
        """
        return self.__row_number

    # Import/Export

    def to_str(self):
        """
        Returns:
            str: a row as a CSV string
        """
        cells = []
        for field in self.__schema.fields:
            if field.name in self:
                cell, notes = field.write_cell(self[field.name])
                cells.append(cell)
        return helpers.stringify_csv_string(cells)

    def to_dict(self, *, json=False):
        """
        Parameters:
            json (bool): make data types compatible with JSON format

        Returns:
            dict: a row as a dictionary
        """
        if json:
            result = {}
            for field in self.__schema.fields:
                if field.name in self:
                    cell = self[field.name]
                    if field.type not in JsonParser.native_types:
                        cell, notes = field.write_cell(cell, ignore_missing=True)
                    if isinstance(cell, Decimal):
                        cell = float(cell)
                    result[field.name] = cell
            return result
        return dict(self)

    def to_list(self, *, json=False):
        """
        Parameters:
            json (bool): make data types compatible with JSON format

        Returns:
            dict: a row as a list
        """
        if json:
            result = []
            for field in self.__schema.fields:
                if field.name in self:
                    cell = self[field.name]
                    if field.type not in JsonParser.native_types:
                        cell, notes = field.write_cell(cell, ignore_missing=True)
                    if isinstance(cell, Decimal):
                        cell = float(cell)
                    result.append(cell)
            return result
        return list(self.values())

    # Process

    def __process(self, key=None):
        #  print('validate')
        cells = self.__cells
        fields = self.__schema.fields
        field_positions = self.__field_positions

        # Type/Constraint error
        for field_name in [key] if key else self.__schema.field_names:
            field, field_position, field_number = self.__field_map[field_name]

            # Read cell
            # TODO: recover
            #  source = None
            #  if len(self.__cells) >= field_number:
            source = self.__cells[field_number - 1]
            target, notes = field.read_cell(source)
            type_note = notes.pop("type", None) if notes else None
            if target is None and not type_note:
                self.__blank_cells[field.name] = source

            # Type error
            if type_note:
                self.__error_cells[field.name] = source
                self.__errors.append(
                    errors.TypeError(
                        note=type_note,
                        cells=list(map(str, self.__cells)),
                        row_number=self.__row_number,
                        row_position=self.__row_position,
                        cell=str(source),
                        field_name=field.name,
                        field_number=field_number,
                        field_position=field_position,
                    )
                )

            # Constraint errors
            if notes:
                for note in notes.values():
                    self.__errors.append(
                        errors.ConstraintError(
                            note=note,
                            cells=list(map(str, self.__cells)),
                            row_number=self.__row_number,
                            row_position=self.__row_position,
                            cell=str(source),
                            field_name=field.name,
                            field_number=field_number,
                            field_position=field_position,
                        )
                    )

            # Set/return value
            self[field.name] = target
            if key:
                return target

        # Extra cells
        if len(fields) < len(cells):
            iterator = cells[len(fields) :]
            start = max(field_positions[: len(fields)]) + 1
            for field_position, cell in enumerate(iterator, start=start):
                self.__errors.append(
                    errors.ExtraCellError(
                        note="",
                        cells=list(map(str, cells)),
                        row_number=self.__row_number,
                        row_position=self.__row_position,
                        cell=str(cell),
                        field_name="",
                        field_number=len(fields) + field_position - start,
                        field_position=field_position,
                    )
                )

        # Missing cells
        if len(fields) > len(cells):
            start = len(cells) + 1
            iterator = zip_longest(field_positions[len(cells) :], fields[len(cells) :])
            for field_number, (field_position, field) in enumerate(iterator, start=start):
                if field is not None:
                    self.__errors.append(
                        errors.MissingCellError(
                            note="",
                            cells=list(map(str, cells)),
                            row_number=self.__row_number,
                            row_position=self.__row_position,
                            cell="",
                            field_name=field.name,
                            field_number=field_number,
                            field_position=field_position
                            or max(field_positions) + field_number - start + 1,
                        )
                    )

        # Blank row
        if len(fields) == len(self.__blank_cells):
            self.__errors = [
                errors.BlankRowError(
                    note="",
                    cells=list(map(str, cells)),
                    row_number=self.__row_number,
                    row_position=self.__row_position,
                )
            ]

        # Set partial flag
        self.__partial = False
