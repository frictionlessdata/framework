from .data import DataError


class TableError(DataError):
    code = "table-error"
    name = "Table Error"
    tags = ["#table"]
    template = "General table error: {note}"
    description = "There is a table error."


class FieldCountError(TableError):
    code = "field-count"
    name = "Field Count Error"
    template = "The data source does not match the expected field count: {note}"
    description = "This error can happen if the data is corrupted."


class RowCountError(TableError):
    code = "row-count"
    name = "Row Count Error"
    template = "The data source does not match the expected row count: {note}"
    description = "This error can happen if the data is corrupted."


class TableDimensionsError(TableError):
    code = "table-dimensions"
    name = "Table dimensions error"
    template = "The data source does not have the required dimensions: {note}"
    description = "This error can happen if the data is corrupted."


class DeviatedValueError(TableError):
    code = "deviated-value"
    name = "Deviated Value"
    template = "There is a possible error because the value is deviated: {note}"
    description = "The value is deviated."


class DeviatedCellError(TableError):
    code = "deviated-cell"
    name = "Deviated cell"
    template = "There is a possible error because the cell is deviated: {note}"
    description = "The cell is deviated."