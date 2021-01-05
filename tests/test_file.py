from frictionless.file import File


# General


BASEURL = "https://raw.githubusercontent.com/frictionlessdata/frictionless-py/master"


def test_file_type_table():
    path = "data/table.csv"
    file = File(path)
    assert file.path == path
    assert file.data is None
    assert file.name == "table"
    assert file.type == "table"
    assert file.scheme == "file"
    assert file.format == "csv"
    assert file.compression == "no"
    assert file.compression_path == ""
    assert file.inline is False
    assert file.remote is False
    assert file.multipart is False
    assert file.basepath == ""
    assert file.fullpath == "data/table.csv"


def test_file_type_general_inline():
    data = [["id", "name"], [1, "english"], [2, "german"]]
    file = File(data)
    assert file.path is None
    assert file.data == data
    assert file.name == "inline"
    assert file.type == "table"
    assert file.scheme == ""
    assert file.format == "inline"
    assert file.compression == "no"
    assert file.compression_path == ""
    assert file.inline is True
    assert file.remote is False
    assert file.multipart is False
    assert file.basepath == ""
    assert file.fullpath is None


def test_file_type_general_remote():
    path = f"{BASEURL}/data/table.csv"
    file = File(path)
    assert file.path == path
    assert file.data is None
    assert file.name == "table"
    assert file.type == "table"
    assert file.scheme == "https"
    assert file.format == "csv"
    assert file.compression == "no"
    assert file.compression_path == ""
    assert file.inline is False
    assert file.remote is True
    assert file.multipart is False
    assert file.basepath == ""
    assert file.fullpath == path


def test_file_type_general_remote_with_basepath():
    path = "data/table.csv"
    file = File(path, basepath=BASEURL)
    assert file.path == path
    assert file.data is None
    assert file.name == "table"
    assert file.type == "table"
    assert file.scheme == "https"
    assert file.format == "csv"
    assert file.compression == "no"
    assert file.compression_path == ""
    assert file.inline is False
    assert file.remote is True
    assert file.multipart is False
    assert file.basepath == BASEURL
    assert file.fullpath == f"{BASEURL}/data/table.csv"


def test_file_type_general_multipart():
    path = ["data/chunk1.csv", "data/chunk2.csv"]
    file = File(path)
    assert file.path == path
    assert file.data is None
    assert file.name == "chunk1"
    assert file.type == "table"
    assert file.scheme == "multipart"
    assert file.format == "csv"
    assert file.compression == "no"
    assert file.compression_path == ""
    assert file.inline is False
    assert file.remote is False
    assert file.multipart is True
    assert file.basepath == ""
    assert file.fullpath == path


def test_file_type_general_multipart_with_basepath():
    path = ["data/chunk1.csv", "data/chunk2.csv"]
    file = File(path, basepath="base")
    assert file.path == path
    assert file.data is None
    assert file.name == "chunk1"
    assert file.type == "table"
    assert file.scheme == "multipart"
    assert file.format == "csv"
    assert file.compression == "no"
    assert file.compression_path == ""
    assert file.inline is False
    assert file.remote is False
    assert file.multipart is True
    assert file.basepath == "base"
    assert file.fullpath == ["base/data/chunk1.csv", "base/data/chunk2.csv"]


def test_file_type_schema():
    path = "data/schema.json"
    file = File(path)
    assert file.path == path
    assert file.data is None
    assert file.name == "schema"
    assert file.type == "schema"
    assert file.scheme == "file"
    assert file.format == "json"
    assert file.compression == "no"
    assert file.compression_path == ""
    assert file.inline is False
    assert file.remote is False
    assert file.multipart is False
    assert file.basepath == ""
    assert file.fullpath == "data/schema.json"


def test_file_type_resource():
    path = "data/resource.json"
    file = File(path)
    assert file.path == path
    assert file.data is None
    assert file.name == "resource"
    assert file.type == "resource"
    assert file.scheme == "file"
    assert file.format == "json"
    assert file.compression == "no"
    assert file.compression_path == ""
    assert file.inline is False
    assert file.remote is False
    assert file.multipart is False
    assert file.basepath == ""
    assert file.fullpath == "data/resource.json"


def test_file_type_package():
    path = "data/package.json"
    file = File(path)
    assert file.path == path
    assert file.data is None
    assert file.name == "package"
    assert file.type == "package"
    assert file.scheme == "file"
    assert file.format == "json"
    assert file.compression == "no"
    assert file.compression_path == ""
    assert file.inline is False
    assert file.remote is False
    assert file.multipart is False
    assert file.basepath == ""
    assert file.fullpath == "data/package.json"
