from __future__ import annotations
import os
import json
import datetime
import secrets
from pathlib import Path
from typing import Optional, List
from ..exception import FrictionlessException
from ..resource import Resource
from ..package import Package
from .database import Database
from .filesystem import Filesystem
from .interfaces import IQueryData, ITable, IFile
from .. import settings
from .. import helpers
from .. import portals

# TODO: handle method errors?
# TODO: ensure that path is safe for all the methods


class Project:
    is_root: bool
    session: Optional[str]
    public: Path
    private: Path
    database: Database
    filesystem: Filesystem

    def __init__(
        self,
        *,
        basepath: Optional[str] = None,
        session: Optional[str] = None,
        is_root: bool = False,
        connect: bool = False,
    ):
        # Provide authz
        base = Path(basepath or "")
        assert base.is_dir()
        if is_root:
            assert not session
        if not is_root:
            assert session or connect
            if not session:
                session = secrets.token_urlsafe(16)
            if not (base / session).is_dir():
                if not connect:
                    raise FrictionlessException("not authorized access")
                session = secrets.token_urlsafe(16)

        # Ensure structure
        public = base / (session or "")
        private = public / ".frictionless"
        database = private / "project.db"
        public.mkdir(parents=True, exist_ok=True)
        private.mkdir(parents=True, exist_ok=True)

        # Store attributes
        self.is_root = is_root
        self.session = session
        self.public = public
        self.private = private
        self.database = Database(f"sqlite:///{database}")
        self.filesystem = Filesystem(str(self.public))

    # General

    def index(self):
        pass

    def query(self, query: str) -> IQueryData:
        return self.database.query(query)

    def query_table(self, query: str) -> ITable:
        return self.database.query_table(query)

    # File

    def count_files(self):
        return len(self.filesystem.list_files())

    def copy_file(self, path: str, *, folder: Optional[str] = None) -> str:
        return self.filesystem.copy_file(path, folder=folder)

    def create_file(
        self, name: str, *, bytes: bytes, folder: Optional[str] = None
    ) -> str:
        return self.filesystem.create_file(name, bytes=bytes, folder=folder)

    def delete_file(self, path: str) -> str:
        self.filesystem.delete_file(path)
        self.database.delete_file(path)
        return path

    # TODO: implement
    def index_file(self, path: str):
        pass

    def list_files(self) -> List[IFile]:
        items = self.filesystem.list_files()
        for item in items:
            if item["path"] == "datapackage.json":
                item["type"] = "package"
        return items

    def move_file(self, path: str, *, folder: str) -> str:
        return self.filesystem.move_file(path, folder=folder)

    # TODO: index if exists but not indexed?
    def read_file(self, path: str) -> Optional[IFile]:
        return self.database.read_file(path)

    # TODO: add read_file_text/data?
    def read_file_bytes(self, path: str) -> bytes:
        return self.filesystem.read_file_bytes(path)

    def read_file_table(
        self,
        path: str,
        *,
        valid: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> ITable:
        return self.database.read_file_table(
            path, valid=valid, limit=limit, offset=offset
        )

    def rename_file(self, path: str, *, name: str) -> str:
        source = path
        target = self.filesystem.rename_file(path, name=name)
        self.database.move_file(source, target)
        return target

    # TODO: implement
    def update_file(self, path: str):
        pass

    # Folder

    def create_folder(self, name: str, *, folder: Optional[str] = None) -> str:
        return self.filesystem.create_folder(name, folder=folder)

    # Package

    def create_package(self):
        path = str(self.public / settings.PACKAGE_PATH)
        if not os.path.exists(path):
            helpers.write_file(path, json.dumps({"resource": []}))
        path = str(Path(path).relative_to(self.public))
        return path

    def publish_package(self, **params):
        response = {}
        controls = {
            "github": portals.GithubControl,
            "zenodo": portals.ZenodoControl,
            "ckan": portals.CkanControl,
        }
        control_type = params["type"]
        allow_update = params["allow_update"]

        del params["type"]
        del params["sandbox"]
        if not allow_update:
            del params["allow_update"]

        package = Package(str(self.public / settings.PACKAGE_PATH))
        if not package.name and not allow_update:
            now = datetime.datetime.now()
            date_time = now.strftime("%H-%M-%S")
            package.name = f"test_package_{date_time}"

        control = controls.get(control_type)
        if not control:
            response["error"] = "Matching control[Github|Zenodo|CKAN] not found"
            return response
        try:
            if "url" in params:
                target = params["url"]
                del params["url"]
                result = package.publish(target=target, control=control(**params))
            else:
                result = package.publish(control=control(**params))
            if control_type == "github":
                result = result.full_name
            response["url"] = result
        except FrictionlessException as exception:
            response["error"] = exception.error.message

        return response
