import os
import sys
import pytest
from frictionless import Table, FrictionlessException


# Environment


# In forked pull requests `.google.json` will not be available
pytestmark = pytest.mark.skipif(
    not os.path.isfile(".google.json"), reason="Google environment is not available"
)


# Parser


@pytest.mark.ci
def test_table_gsheets():
    source = "https://docs.google.com/spreadsheets/d/1mHIWnDvW9cALRMq9OdNfRwjAthCUFUOACPp0Lkyl7b4/edit?usp=sharing"
    with Table(source) as table:
        assert table.header == ["id", "name"]
        assert table.read_data() == [["1", "english"], ["2", "中国人"]]


@pytest.mark.ci
def test_table_gsheets_with_gid():
    source = "https://docs.google.com/spreadsheets/d/1mHIWnDvW9cALRMq9OdNfRwjAthCUFUOACPp0Lkyl7b4/edit#gid=960698813"
    with Table(source) as table:
        assert table.header == ["id", "name"]
        assert table.read_data() == [["2", "中国人"], ["3", "german"]]


@pytest.mark.ci
def test_table_gsheets_bad_url():
    table = Table("https://docs.google.com/spreadsheets/d/bad")
    with pytest.raises(FrictionlessException) as excinfo:
        table.open()
    error = excinfo.value.error
    assert error.code == "scheme-error"
    assert error.note.count("404 Client Error: Not Found for url")


@pytest.mark.ci
@pytest.mark.skipif(sys.version_info < (3, 8), reason="Speed up CI")
def test_table_gsheets_write():
    path = "https://docs.google.com/spreadsheets/d/1F2OiYmaf8e3x7jSc95_uNgfUyBlSXrcRg-4K_MFNZQI/edit"

    # Write
    with Table("data/table.csv") as table:
        table.write(path, dialect={"credentials": ".google.json"})

    # Read
    with Table(path) as table:
        assert table.header == ["id", "name"]
        assert table.read_data() == [["1", "english"], ["2", "中国人"]]
