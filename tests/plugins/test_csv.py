import pytest
from frictionless import Table, helpers
from frictionless.plugins.csv import CsvDialect

BASE_URL = "https://raw.githubusercontent.com/okfn/tabulator-py/master/%s"


# Read


def test_csv_parser():
    with Table("data/table.csv") as table:
        assert table.header == ["id", "name"]
        assert table.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


def test_csv_parser_with_bom():
    with Table("data/bom.csv") as table:
        assert table.header == ["id", "name"]
        assert table.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


def test_csv_parser_with_bom_with_encoding():
    with Table("data/bom.csv", encoding="utf-8") as table:
        assert table.header == ["id", "name"]
        assert table.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


def test_csv_parser_excel():
    source = "header1,header2\nvalue1,value2\nvalue3,value4"
    with Table(source, scheme="text", format="csv") as table:
        assert table.header == ["header1", "header2"]
        assert table.read_rows() == [
            {"header1": "value1", "header2": "value2"},
            {"header1": "value3", "header2": "value4"},
        ]


def test_csv_parser_excel_tab():
    source = "header1\theader2\nvalue1\tvalue2\nvalue3\tvalue4"
    dialect = CsvDialect(delimiter="\t")
    with Table(source, scheme="text", format="csv", dialect=dialect) as table:
        assert table.header == ["header1", "header2"]
        assert table.read_rows() == [
            {"header1": "value1", "header2": "value2"},
            {"header1": "value3", "header2": "value4"},
        ]


def test_csv_parser_unix():
    source = '"header1","header2"\n"value1","value2"\n"value3","value4"'
    with Table(source, scheme="text", format="csv") as table:
        assert table.header == ["header1", "header2"]
        assert table.read_rows() == [
            {"header1": "value1", "header2": "value2"},
            {"header1": "value3", "header2": "value4"},
        ]


def test_csv_parser_escaping():
    dialect = CsvDialect(escape_char="\\")
    with Table("data/escaping.csv", dialect=dialect) as table:
        assert table.header == ["ID", "Test"]
        assert table.read_rows() == [
            {"ID": 1, "Test": "Test line 1"},
            {"ID": 2, "Test": 'Test " line 2'},
            {"ID": 3, "Test": 'Test " line 3'},
        ]


def test_csv_parser_doublequote():
    with Table("data/doublequote.csv") as table:
        assert len(table.header) == 17
        for row in table:
            assert len(row) == 17


def test_csv_parser_stream():
    source = open("data/table.csv", mode="rb")
    with Table(source, format="csv") as table:
        assert table.header == ["id", "name"]
        assert table.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


def test_csv_parser_text():
    source = "text://id,name\n1,english\n2,中国人\n"
    with Table(source, format="csv") as table:
        assert table.header == ["id", "name"]
        assert table.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


@pytest.mark.vcr
def test_csv_parser_remote():
    with Table(BASE_URL % "data/table.csv") as table:
        assert table.header == ["id", "name"]
        assert table.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


@pytest.mark.vcr
def test_csv_parser_remote_non_ascii_url():
    source = "http://data.defra.gov.uk/ops/government_procurement_card/over_£500_GPC_apr_2013.csv"
    with Table(source) as table:
        assert table.header == [
            "Entity",
            "Transaction Posting Date",
            "Merchant Name",
            "Amount",
            "Description",
        ]


def test_csv_parser_delimiter():
    source = '"header1";"header2"\n"value1";"value2"\n"value3";"value4"'
    dialect = CsvDialect(delimiter=";")
    with Table(source, scheme="text", format="csv", dialect=dialect) as table:
        assert table.header == ["header1", "header2"]
        assert table.read_rows() == [
            {"header1": "value1", "header2": "value2"},
            {"header1": "value3", "header2": "value4"},
        ]


def test_csv_parser_escapechar():
    source = "header1%,header2\nvalue1%,value2\nvalue3%,value4"
    dialect = CsvDialect(escape_char="%")
    with Table(source, scheme="text", format="csv", dialect=dialect) as table:
        assert table.header == ["header1,header2"]
        assert table.read_rows() == [
            {"header1,header2": "value1,value2"},
            {"header1,header2": "value3,value4"},
        ]


def test_csv_parser_quotechar():
    source = "%header1,header2%\n%value1,value2%\n%value3,value4%"
    dialect = CsvDialect(quote_char="%")
    with Table(source, scheme="text", format="csv", dialect=dialect) as table:
        assert table.header == ["header1,header2"]
        assert table.read_rows() == [
            {"header1,header2": "value1,value2"},
            {"header1,header2": "value3,value4"},
        ]


def test_csv_parser_skipinitialspace():
    source = "header1, header2\nvalue1, value2\nvalue3, value4"
    dialect = CsvDialect(skip_initial_space=False)
    with Table(source, scheme="text", format="csv", dialect=dialect) as table:
        assert table.header == ["header1", "header2"]
        assert table.read_rows() == [
            {"header1": "value1", "header2": " value2"},
            {"header1": "value3", "header2": " value4"},
        ]


def test_csv_parser_skipinitialspace_default():
    source = "header1, header2\nvalue1, value2\nvalue3, value4"
    with Table(source, scheme="text", format="csv") as table:
        assert table.header == ["header1", "header2"]
        assert table.read_rows() == [
            {"header1": "value1", "header2": "value2"},
            {"header1": "value3", "header2": "value4"},
        ]


def test_csv_parser_detect_delimiter_tab():
    source = "a1\tb1\tc1A,c1B\na2\tb2\tc2\n"
    with Table(source, scheme="text", format="csv", headers=False) as table:
        assert table.read_rows() == [
            {"field1": "a1", "field2": "b1", "field3": "c1A,c1B"},
            {"field1": "a2", "field2": "b2", "field3": "c2"},
        ]


def test_csv_parser_detect_delimiter_semicolon():
    source = "a1;b1\na2;b2\n"
    with Table(source, scheme="text", format="csv", headers=False) as table:
        assert table.read_rows() == [
            {"field1": "a1", "field2": "b1"},
            {"field1": "a2", "field2": "b2"},
        ]


def test_csv_parser_detect_delimiter_pipe():
    source = "a1|b1\na2|b2\n"
    with Table(source, scheme="text", format="csv", headers=False) as table:
        assert table.read_rows() == [
            {"field1": "a1", "field2": "b1"},
            {"field1": "a2", "field2": "b2"},
        ]


def test_csv_parser_dialect_should_not_persist_if_sniffing_fails_issue_goodtables_228():
    source1 = "a;b;c\n#comment"
    source2 = "a,b,c\n#comment"
    dialect = CsvDialect(delimiter=";")
    with Table(source1, scheme="text", format="csv", dialect=dialect) as table:
        assert table.header == ["a", "b", "c"]
    with Table(source2, scheme="text", format="csv") as table:
        assert table.header == ["a", "b", "c"]


def test_csv_parser_quotechar_is_empty_string():
    source = 'header1,header2",header3\nvalue1,value2",value3'
    dialect = CsvDialect(quote_char="")
    with Table(source, scheme="text", format="csv", dialect=dialect) as table:
        table.header == ["header1", 'header2"', "header3"]
        assert table.read_rows() == [
            {"header1": "value1", 'header2"': 'value2"', "header3": "value3"},
        ]


def test_table_format_tsv():
    with Table("data/table.tsv", patch_schema={"missingValues": ["\\N"]}) as table:
        assert table.dialect == {"delimiter": "\t"}
        assert table.header == ["id", "name"]
        assert table.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
            {"id": 3, "name": None},
        ]


# Write


def test_csv_parser_write(tmpdir):
    source = "data/table.csv"
    target = str(tmpdir.join("table.csv"))
    with Table(source) as table:
        table.write(target)
    with Table(target) as table:
        assert table.header == ["id", "name"]
        assert table.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


def test_csv_parser_write_delimiter(tmpdir):
    source = "data/table.csv"
    target = str(tmpdir.join("table.csv"))
    dialect = CsvDialect(delimiter=";")
    with Table(source) as table:
        table.write(target, dialect=dialect)
    with Table(target, dialect=dialect) as table:
        assert table.header == ["id", "name"]
        assert table.dialect == {"delimiter": ";"}
        assert table.read_rows() == [
            {"id": 1, "name": "english"},
            {"id": 2, "name": "中国人"},
        ]


def test_csv_parser_write_inline_source(tmpdir):
    source = [{"key1": "value1", "key2": "value2"}]
    target = str(tmpdir.join("table.csv"))
    with Table(source) as table:
        table.write(target)
    with Table(target) as table:
        assert table.header == ["key1", "key2"]
        assert table.read_rows() == [
            {"key1": "value1", "key2": "value2"},
        ]


@pytest.mark.skipif(helpers.is_platform("windows"), reason="It doesn't work for Windows")
def test_table_tsv_write(tmpdir):
    source = "data/table.csv"
    target = str(tmpdir.join("table.tsv"))
    with Table(source) as table:
        table.write(target)
    with open(target) as file:
        assert file.read() == "id\tname\n1\tenglish\n2\t中国人\n"
