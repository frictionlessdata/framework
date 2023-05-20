from __future__ import annotations
import shutil
from typing import Optional
from pydantic import BaseModel
from fastapi import Request
from ....exception import FrictionlessException
from ...project import Project
from ...router import router


class Props(BaseModel, extra="forbid"):
    path: str
    toPath: Optional[str] = None
    newName: Optional[str] = None
    deduplicate: Optional[bool] = None


class Result(BaseModel, extra="forbid"):
    path: str


@router.post("/file/move")
def server_file_move(request: Request, props: Props) -> Result:
    return action(request.app.get_project(), props)


def action(project: Project, props: Props) -> Result:
    fs = project.filesystem

    # Source
    source = fs.get_fullpath(props.path)
    print(source)
    if not source.exists():
        raise FrictionlessException("Source doesn't exist")

    # Target
    target = source
    if props.toPath:
        target = fs.get_fullpath(props.toPath)
    if props.newName:
        target = target.parent / props.newName
    if target.is_file():
        raise FrictionlessException("Target already exists")
    if target.is_dir():
        target = target / source.name
        if props.deduplicate:
            target = fs.deduplicate_fullpath(target)

    # Move
    shutil.move(source, target)
    path = fs.get_path(target)

    return Result(path=path)
