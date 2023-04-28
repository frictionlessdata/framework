import pytest
from pathlib import Path
from frictionless import helpers
from frictionless.server import Project


name1 = "name1.txt"
name2 = "name2.txt"
name3 = "name3.json"
name4 = "name4.csv"
name5 = "table.csv"
bytes1 = b"bytes1"
bytes2 = b"bytes2"
bytes3 = b'{"key": "value"}'
bytes4 = b"id,name\n1,english\n2,spanish"
bytes5 = b"id,name\n1,english\n2,\xe4\xb8\xad\xe5\x9b\xbd\xe4\xba\xba\n"
folder1 = "folder1"
folder2 = "folder2"
not_secure = ["/path", "../path", "../", "./"]
files = [
    "table.csv",
    "table.json",
    "table.jsonl",
    "table.keyed.json",
    "table.keyed.yaml",
    "table.ndjson",
    "table.tsv",
    "table.xls",
    "table.xlsx",
]
link = "https://raw.githubusercontent.com/fdtester/multiple-file-types/main"


# Create


def test_project_create_file(tmpdir):
    project = Project(tmpdir)
    url = f"{link}/table.csv"
    path = project.create_file(url)
    assert helpers.read_file(tmpdir / name5, "rb") == bytes5
    assert path == name5
    assert project.list_files() == [
        {"path": name5, "type": "table"},
    ]


def test_project_create_file_in_folder(tmpdir):
    project = Project(tmpdir)
    project.create_folder(folder1)
    url = f"{link}/table.csv"
    path = project.create_file(url, folder=folder1)
    assert path == str(Path(folder1) / name5)
    assert helpers.read_file(tmpdir / path, "rb") == bytes5
    assert project.list_files() == [
        {"path": folder1, "type": "folder"},
        {"path": path, "type": "table"},
    ]


@pytest.mark.parametrize("path", not_secure)
def test_project_create_file_security(tmpdir, path):
    project = Project(tmpdir)
    with pytest.raises(Exception):
        project.create_file(path)
    with pytest.raises(Exception):
        project.create_file(name1, folder=path)


@pytest.mark.parametrize("name", files)
@pytest.mark.skipif(reason="Fails with some file types - json, yaml")
def test_project_create_multiple_file_types(tmpdir, name):
    project = Project(tmpdir)
    url = f"{link}/{name}"
    path = project.create_file(url)
    assert path == name
    assert project.list_files() == [
        {"path": name, "type": "table"},
    ]


def test_project_create_file_type_ods(tmpdir):
    project = Project(tmpdir)
    url = "https://github.com/fdtester/multiple-file-types/blob/main/table.ods?raw=true"
    name = "table.ods"
    path = project.create_file(url)
    assert path == name
    assert project.list_files() == [
        {"path": name, "type": "table"},
    ]


# Index


def test_project_index_file(tmpdir):
    project = Project(tmpdir)
    path = project.upload_file(name4, bytes=bytes4)
    file = project.index_file(path)
    assert file
    assert file["path"] == name4
    assert file.get("type") == "table"
    record = file.get("record")
    table = project.query_table("SELECT * FROM name4")
    assert record
    assert record["updated"]
    assert record.get("tableName") == "name4"
    assert record["resource"]["path"] == name4
    assert record["resource"]["schema"]["fields"][0] == dict(name="id", type="integer")
    assert record["resource"]["schema"]["fields"][0] == dict(name="id", type="integer")
    assert record["resource"]["schema"]["fields"][1] == dict(name="name", type="string")
    assert table["tableSchema"]
    assert table["header"] == ["_rowNumber", "_rowValid", "id", "name"]
    assert table["rows"] == [
        {"_rowNumber": 2, "_rowValid": True, "id": 1, "name": "english"},
        {"_rowNumber": 3, "_rowValid": True, "id": 2, "name": "spanish"},
    ]


# Rename


def test_project_rename_file(tmpdir):
    project = Project(tmpdir)
    project.upload_file(name1, bytes=bytes1)
    project.rename_file(name1, name=name2)
    assert project.read_file(name2) == bytes1
    assert project.list_files() == [
        {"path": name2, "type": "text"},
    ]


def test_project_rename_file_folder(tmpdir):
    project = Project(tmpdir)
    project.create_folder(folder1)
    project.upload_file(name1, bytes=bytes1, folder=folder1)
    project.rename_file(folder1, name=folder2)
    assert project.list_files() == [
        {"path": folder2, "type": "folder"},
        {"path": str(Path(folder2) / name1), "type": "text"},
    ]


@pytest.mark.parametrize("path", not_secure)
def test_project_rename_file_security(tmpdir, path):
    project = Project(tmpdir)
    project.upload_file(name1, bytes=bytes1)
    with pytest.raises(Exception):
        project.rename_file(path, name=name2)
    with pytest.raises(Exception):
        project.rename_file(name1, name=path)


# Select


def test_project_select_file(tmpdir):
    project = Project(tmpdir)
    project.upload_file(name1, bytes=bytes1)
    assert project.select_file(name1) == {"path": name1, "type": "text"}
    assert project.list_files() == [
        {"path": name1, "type": "text"},
    ]


@pytest.mark.parametrize("path", not_secure)
def test_project_select_file_security(tmpdir, path):
    project = Project(tmpdir)
    with pytest.raises(Exception):
        project.select_file(path)
