from __future__ import annotations
import shutil
from typing import Optional
from pydantic import BaseModel
from fastapi import Request
from ....resource import Resource
from ....exception import FrictionlessException
from ...project import Project
from ...router import router
from ... import helpers


class Props(BaseModel, extra="forbid"):
    path: str
    toPath: Optional[str] = None
    deduplicate: Optional[bool] = None


class Result(BaseModel, extra="forbid"):
    path: str


@router.post("/file/copy")
def endpoint(request: Request, props: Props) -> Result:
    return action(request.app.get_project(), props)


def action(project: Project, props: Props) -> Result:
    fs = project.filesystem
    md = project.metadata

    # Get source
    source = fs.get_fullpath(props.path)
    if not source.exists():
        raise FrictionlessException("Source doesn't exist")

    # Get target
    target = fs.get_fullpath(props.toPath) if props.toPath else fs.basepath
    if target.is_file():
        raise FrictionlessException("Target already exists")
    if target.is_dir():
        target = target / source.name
        if props.deduplicate:
            target = fs.deduplicate_fullpath(target, suffix="copy")

    # Copy file
    copy = shutil.copytree if source.is_dir() else shutil.copy
    copy(source, target)
    path = fs.get_path(target)

    # Copy record
    record = helpers.read_record(project, path=props.path)
    if record:
        record.name = helpers.make_record_name(project, resource=Resource(path=path))
        record.path = path
        record.resource["path"] = path
        md.write_document(name=record.name, type="record", descriptor=record.dict())

    path = fs.get_path(target)
    return Result(path=path)
