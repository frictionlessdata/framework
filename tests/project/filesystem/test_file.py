import pytest
from pathlib import Path
from frictionless import Filesystem, helpers


name1 = "name1.txt"
name2 = "name2.txt"
bytes1 = b"bytes1"
bytes2 = b"bytes2"
bytes3 = b'{"key": "value"}'
folder1 = "folder1"
folder2 = "folder2"
not_secure = ["/path", "../path", "../", "./"]


# Copy


def test_fs_copy_file(tmpdir):
    name1copy = "name1 (copy1).txt"
    fs = Filesystem(tmpdir)
    fs.create_file(name1, bytes=bytes1)
    path = fs.copy_file(name1)
    assert path == name1copy
    assert fs.read_file(name1) == bytes1
    assert fs.read_file(name1copy) == bytes1
    assert fs.list_files() == [
        {"path": name1copy, "isFolder": False},
        {"path": name1, "isFolder": False},
    ]


def test_fs_copy_file_to_folder(tmpdir):
    fs = Filesystem(tmpdir)
    fs.create_file(name1, bytes=bytes1)
    fs.create_folder(folder1)
    path = fs.copy_file(name1, folder=folder1)
    assert path == str(Path(folder1) / name1)
    assert fs.read_file(name1) == bytes1
    assert fs.read_file(path) == bytes1
    assert fs.list_files() == [
        {"path": folder1, "isFolder": True},
        {"path": path, "isFolder": False},
        {"path": name1, "isFolder": False},
    ]


def test_fs_copy_file_from_folder_to_folder(tmpdir):
    path1 = str(Path(folder1) / name1)
    path2 = str(Path(folder2) / folder1 / name1)
    fs = Filesystem(tmpdir)
    fs.create_folder(folder1)
    fs.create_folder(folder2)
    fs.create_file(name1, bytes=bytes1, folder=folder1)
    path = fs.copy_file(folder1, folder=folder2)
    assert path == str(Path(folder2) / folder1)
    assert helpers.read_file(tmpdir / path1, "rb") == bytes1
    assert helpers.read_file(tmpdir / path2, "rb") == bytes1
    assert fs.list_files() == [
        {"path": folder1, "isFolder": True},
        {"path": path1, "isFolder": False},
        {"path": folder2, "isFolder": True},
        {"path": str(Path(folder2) / folder1), "isFolder": True},
        {"path": str(Path(folder2) / folder1 / name1), "isFolder": False},
    ]


@pytest.mark.parametrize("path", not_secure)
def test_fs_copy_file_security(tmpdir, path):
    fs = Filesystem(tmpdir)
    fs.create_file(name1, bytes=bytes1)
    with pytest.raises(Exception):
        fs.copy_file(path)
    with pytest.raises(Exception):
        fs.copy_file(name1, folder=path)


# Create


def test_fs_create_file(tmpdir):
    fs = Filesystem(tmpdir)
    path = fs.create_file(name1, bytes=bytes1)
    assert helpers.read_file(tmpdir / name1, "rb") == bytes1
    assert path == name1
    assert fs.list_files() == [
        {"path": name1, "isFolder": False},
    ]


def test_fs_create_file_in_folder(tmpdir):
    fs = Filesystem(tmpdir)
    fs.create_folder(folder1)
    path = fs.create_file(name1, bytes=bytes1, folder=folder1)
    assert path == str(Path(folder1) / name1)
    assert helpers.read_file(tmpdir / path, "rb") == bytes1
    assert fs.list_files() == [
        {"path": folder1, "isFolder": True},
        {"path": path, "isFolder": False},
    ]


@pytest.mark.parametrize("path", not_secure)
def test_fs_create_file_security(tmpdir, path):
    fs = Filesystem(tmpdir)
    with pytest.raises(Exception):
        fs.create_file(path, bytes=bytes1)
    with pytest.raises(Exception):
        fs.create_file(name1, bytes=bytes1, folder=path)


# Delete


def test_fs_delete_file(tmpdir):
    fs = Filesystem(tmpdir)
    fs.create_file(name1, bytes=bytes1)
    fs.create_file(name2, bytes=bytes2)
    fs.delete_file(name2)
    assert fs.list_files() == [
        {"path": name1, "isFolder": False},
    ]


def test_fs_delete_file_folder(tmpdir):
    fs = Filesystem(tmpdir)
    fs.create_folder(folder1)
    fs.create_file(name1, bytes=bytes1, folder=folder1)
    fs.delete_file(folder1)
    assert fs.list_files() == []


@pytest.mark.parametrize("path", not_secure)
def test_fs_delete_file_security(tmpdir, path):
    fs = Filesystem(tmpdir)
    with pytest.raises(Exception):
        fs.delete_file(path)


# List


def test_fs_list_files(tmpdir):
    fs = Filesystem(tmpdir)
    fs.create_file(name1, bytes=bytes1)
    fs.create_file(name2, bytes=bytes2)
    assert fs.list_files() == [
        {"path": name1, "isFolder": False},
        {"path": name2, "isFolder": False},
    ]


def test_fs_list_files_with_folders(tmpdir):
    fs = Filesystem(tmpdir)
    fs.create_file(name1, bytes=bytes1)
    fs.create_folder(folder1)
    assert fs.list_files() == [
        {"path": folder1, "isFolder": True},
        {"path": name1, "isFolder": False},
    ]


# Move


def test_fs_move_file(tmpdir):
    fs = Filesystem(tmpdir)
    fs.create_file(name1, bytes=bytes1)
    fs.create_folder(folder1)
    path = fs.move_file(name1, folder=folder1)
    print(path)
    assert path == str(Path(folder1) / name1)
    assert fs.read_file(path) == bytes1
    assert fs.list_files() == [
        {"path": folder1, "isFolder": True},
        {"path": path, "isFolder": False},
    ]


def test_fs_move_file_folder(tmpdir):
    path2 = str(Path(folder2) / folder1 / name1)
    fs = Filesystem(tmpdir)
    fs.create_folder(folder1)
    fs.create_folder(folder2)
    fs.create_file(name1, bytes=bytes1, folder=folder1)
    path = fs.move_file(folder1, folder=folder2)
    assert path == str(Path(folder2) / folder1)
    assert helpers.read_file(tmpdir / path2, "rb") == bytes1
    assert fs.list_files() == [
        {"path": folder2, "isFolder": True},
        {"path": str(Path(folder2) / folder1), "isFolder": True},
        {"path": str(Path(folder2) / folder1 / name1), "isFolder": False},
    ]


@pytest.mark.parametrize("path", not_secure)
def test_fs_move_file_security(tmpdir, path):
    fs = Filesystem(tmpdir)
    fs.create_file(name1, bytes=bytes1)
    with pytest.raises(Exception):
        fs.move_file(path, folder=folder1)
    with pytest.raises(Exception):
        fs.move_file(name1, folder=path)


# Read


def test_fs_read_file(tmpdir):
    fs = Filesystem(tmpdir)
    fs.create_file(name1, bytes=bytes1)
    assert fs.read_file(name1) == bytes1
    assert fs.list_files() == [
        {"path": name1, "isFolder": False},
    ]


@pytest.mark.parametrize("path", not_secure)
def test_fs_read_file_security(tmpdir, path):
    fs = Filesystem(tmpdir)
    with pytest.raises(Exception):
        fs.read_file(path)


# Rename


def test_fs_rename_file(tmpdir):
    fs = Filesystem(tmpdir)
    fs.create_file(name1, bytes=bytes1)
    fs.rename_file(name1, name=name2)
    assert fs.read_file(name2) == bytes1
    assert fs.list_files() == [
        {"path": name2, "isFolder": False},
    ]


def test_fs_rename_file_folder(tmpdir):
    fs = Filesystem(tmpdir)
    fs.create_folder(folder1)
    fs.create_file(name1, bytes=bytes1, folder=folder1)
    fs.rename_file(folder1, name=folder2)
    assert fs.list_files() == [
        {"path": folder2, "isFolder": True},
        {"path": str(Path(folder2) / name1), "isFolder": False},
    ]


@pytest.mark.parametrize("path", not_secure)
def test_fs_rename_file_security(tmpdir, path):
    fs = Filesystem(tmpdir)
    fs.create_file(name1, bytes=bytes1)
    with pytest.raises(Exception):
        fs.rename_file(path, name=name2)
    with pytest.raises(Exception):
        fs.rename_file(name1, name=path)
