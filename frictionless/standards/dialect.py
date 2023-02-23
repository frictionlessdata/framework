from __future__ import annotations
from typing import List, Union, Literal
from typing_extensions import Required, TypedDict


class IDialect(TypedDict, total=False):
    name: str
    title: str
    description: str
    header: bool
    headerRows: List[int]
    headerJoin: str
    headerCase: bool
    commentChar: str
    commentRows: List[int]
    skipBlankRows: bool
    csv: ICsvControl
    json: IJsonControl
    excel: IExcelControl


class IBaseControl(TypedDict, total=False):
    title: str
    description: str


class ICsvControl(IBaseControl, total=False):
    delimiter: str
    lineTerminator: str
    quoteChar: str
    doubleQuote: bool
    escapeChar: str
    nullSequence: str
    skipInitialSpace: bool


class IJsonControl(IBaseControl, total=False):
    keys: List[str]
    keyed: bool
    property: str


class IExcelControl(IBaseControl, total=False):
    sheet: Union[str, int]
    fillMergedCells: bool
    preserveFormatting: bool
    adjustFloatingPointError: bool
    stringified: bool
