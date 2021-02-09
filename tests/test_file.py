import pytest
from pathlib import Path
from frictionless import system, helpers


# General


BASEURL = "https://raw.githubusercontent.com/frictionlessdata/frictionless-py/master"


def test_file_type_table():
    path = "data/table.csv"
    file = system.create_file(path)
    assert file.path == path
    assert file.data is None
    assert file.name == "table"
    assert file.type == "table"
    assert file.scheme == "file"
    assert file.format == "csv"
    assert file.innerpath == ""
    assert file.compression == ""
    assert file.memory is False
    assert file.remote is False
    assert file.multipart is False
    assert file.basepath == ""
    assert file.fullpath == "data/table.csv"


def test_file_type_table_compression():
    path = "data/table.csv.gz"
    file = system.create_file(path)
    assert file.path == path
    assert file.data is None
    assert file.name == "table"
    assert file.type == "table"
    assert file.scheme == "file"
    assert file.format == "csv"
    assert file.innerpath == ""
    assert file.compression == "gz"
    assert file.memory is False
    assert file.remote is False
    assert file.multipart is False
    assert file.basepath == ""
    assert file.fullpath == "data/table.csv.gz"


def test_file_memory():
    data = [["id", "name"], [1, "english"], [2, "german"]]
    file = system.create_file(data)
    assert file.path is None
    assert file.data == data
    assert file.name == "memory"
    assert file.type == "table"
    assert file.scheme == ""
    assert file.format == "inline"
    assert file.innerpath == ""
    assert file.compression == ""
    assert file.memory is True
    assert file.remote is False
    assert file.multipart is False
    assert file.basepath == ""
    assert file.fullpath is None


def test_file_remote():
    path = f"{BASEURL}/data/table.csv"
    file = system.create_file(path)
    assert file.path == path
    assert file.data is None
    assert file.name == "table"
    assert file.type == "table"
    assert file.scheme == "https"
    assert file.format == "csv"
    assert file.innerpath == ""
    assert file.compression == ""
    assert file.memory is False
    assert file.remote is True
    assert file.multipart is False
    assert file.basepath == ""
    assert file.fullpath == path


@pytest.mark.skipif(helpers.is_platform("windows"), reason="It doesn't work for Windows")
def test_file_remote_with_basepath():
    path = "data/table.csv"
    file = system.create_file(path, basepath=BASEURL)
    assert file.path == path
    assert file.data is None
    assert file.name == "table"
    assert file.type == "table"
    assert file.scheme == "https"
    assert file.format == "csv"
    assert file.innerpath == ""
    assert file.compression == ""
    assert file.memory is False
    assert file.remote is True
    assert file.multipart is False
    assert file.basepath == BASEURL
    assert file.fullpath == f"{BASEURL}/data/table.csv"


def test_file_multipart():
    path = ["data/chunk1.csv", "data/chunk2.csv"]
    file = system.create_file(path)
    assert file.path == path
    assert file.data is None
    assert file.name == "chunk"
    assert file.type == "table"
    assert file.scheme == "multipart"
    assert file.format == "csv"
    assert file.innerpath == ""
    assert file.compression == ""
    assert file.memory is False
    assert file.remote is False
    assert file.multipart is True
    assert file.basepath == ""
    assert file.fullpath == path


@pytest.mark.skipif(helpers.is_platform("windows"), reason="It doesn't work for Windows")
def test_file_multipart_with_basepath():
    path = ["data/chunk1.csv", "data/chunk2.csv"]
    file = system.create_file(path, basepath="base")
    assert file.path == path
    assert file.data is None
    assert file.name == "chunk"
    assert file.type == "table"
    assert file.scheme == "multipart"
    assert file.format == "csv"
    assert file.innerpath == ""
    assert file.compression == ""
    assert file.memory is False
    assert file.remote is False
    assert file.multipart is True
    assert file.basepath == "base"
    assert file.fullpath == ["base/data/chunk1.csv", "base/data/chunk2.csv"]


@pytest.mark.skipif(helpers.is_platform("windows"), reason="It doesn't work for Windows")
def test_file_multipart_from_glob():
    path = "data/tables/chunk*.csv"
    file = system.create_file(path)
    assert file.path == path
    assert file.data is None
    assert file.name == "chunk"
    assert file.type == "table"
    assert file.scheme == "multipart"
    assert file.format == "csv"
    assert file.innerpath == ""
    assert file.compression == ""
    assert file.memory is False
    assert file.remote is False
    assert file.multipart is True
    assert file.expandable is True
    assert file.basepath == ""
    assert file.normpath == ["data/tables/chunk1.csv", "data/tables/chunk2.csv"]
    assert file.fullpath == ["data/tables/chunk1.csv", "data/tables/chunk2.csv"]


@pytest.mark.skipif(helpers.is_platform("windows"), reason="It doesn't work for Windows")
def test_file_multipart_from_glob_with_basepath():
    path = "chunk*.csv"
    file = system.create_file(path, basepath="data/tables")
    assert file.path == path
    assert file.data is None
    assert file.name == "chunk"
    assert file.type == "table"
    assert file.scheme == "multipart"
    assert file.format == "csv"
    assert file.innerpath == ""
    assert file.compression == ""
    assert file.memory is False
    assert file.remote is False
    assert file.multipart is True
    assert file.expandable is True
    assert file.basepath == "data/tables"
    assert file.normpath == ["chunk1.csv", "chunk2.csv"]
    assert file.fullpath == ["data/tables/chunk1.csv", "data/tables/chunk2.csv"]


@pytest.mark.skipif(helpers.is_platform("windows"), reason="It doesn't work for Windows")
def test_file_multipart_from_dir():
    path = "data/tables"
    file = system.create_file(path)
    assert file.path == path
    assert file.data is None
    assert file.name == "chunk"
    assert file.type == "table"
    assert file.scheme == "multipart"
    assert file.format == "csv"
    assert file.innerpath == ""
    assert file.compression == ""
    assert file.memory is False
    assert file.remote is False
    assert file.multipart is True
    assert file.expandable is True
    assert file.basepath == ""
    assert file.normpath == ["data/tables/chunk1.csv", "data/tables/chunk2.csv"]
    assert file.fullpath == ["data/tables/chunk1.csv", "data/tables/chunk2.csv"]


@pytest.mark.skipif(helpers.is_platform("windows"), reason="It doesn't work for Windows")
def test_file_multipart_from_dir_with_basepath():
    path = "tables"
    file = system.create_file(path, basepath="data")
    assert file.path == path
    assert file.data is None
    assert file.name == "chunk"
    assert file.type == "table"
    assert file.scheme == "multipart"
    assert file.format == "csv"
    assert file.innerpath == ""
    assert file.compression == ""
    assert file.memory is False
    assert file.remote is False
    assert file.multipart is True
    assert file.expandable is True
    assert file.basepath == "data"
    assert file.normpath == ["tables/chunk1.csv", "tables/chunk2.csv"]
    assert file.fullpath == ["data/tables/chunk1.csv", "data/tables/chunk2.csv"]


def test_file_schema():
    path = "data/schema.json"
    file = system.create_file(path)
    assert file.path == path
    assert file.data is None
    assert file.name == "schema"
    assert file.type == "schema"
    assert file.scheme == "file"
    assert file.format == "json"
    assert file.innerpath == ""
    assert file.compression == ""
    assert file.memory is False
    assert file.remote is False
    assert file.multipart is False
    assert file.basepath == ""
    assert file.fullpath == "data/schema.json"


def test_file_resource():
    path = "data/resource.json"
    file = system.create_file(path)
    assert file.path == path
    assert file.data is None
    assert file.name == "resource"
    assert file.type == "resource"
    assert file.scheme == "file"
    assert file.format == "json"
    assert file.innerpath == ""
    assert file.compression == ""
    assert file.memory is False
    assert file.remote is False
    assert file.multipart is False
    assert file.basepath == ""
    assert file.fullpath == "data/resource.json"


def test_file_package():
    path = "data/package.json"
    file = system.create_file(path)
    assert file.path == path
    assert file.data is None
    assert file.name == "package"
    assert file.type == "package"
    assert file.scheme == "file"
    assert file.format == "json"
    assert file.innerpath == ""
    assert file.compression == ""
    assert file.memory is False
    assert file.remote is False
    assert file.multipart is False
    assert file.basepath == ""
    assert file.fullpath == "data/package.json"


@pytest.mark.skipif(helpers.is_platform("windows"), reason="It doesn't work for Windows")
def test_file_package_from_pathlib():
    path = Path("data/package.json")
    file = system.create_file(path)
    assert file.path == str(path)
    assert file.data is None
    assert file.name == "package"
    assert file.type == "package"
    assert file.scheme == "file"
    assert file.format == "json"
    assert file.innerpath == ""
    assert file.compression == ""
    assert file.memory is False
    assert file.remote is False
    assert file.multipart is False
    assert file.basepath == ""
    assert file.fullpath == "data/package.json"
