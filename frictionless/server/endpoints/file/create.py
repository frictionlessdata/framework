from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from fastapi import Request, UploadFile, File, Form
from ....exception import FrictionlessException
from ...project import Project
from ...router import router
from ... import helpers


class Props(BaseModel):
    path: str
    bytes: bytes
    folder: Optional[str] = None
    deduplicate: Optional[bool] = None


class Result(BaseModel):
    path: str


@router.post("/file/create")
async def endpoint(
    request: Request,
    file: UploadFile = File(),
    path: Optional[str] = Form(None),
    folder: Optional[str] = Form(None),
    deduplicate: Optional[bool] = Form(None),
) -> Result:
    bytes = await file.read()
    path = path or file.filename or "name"
    return action(
        request.app.get_project(),
        Props(path=path, bytes=bytes, folder=folder, deduplicate=deduplicate),
    )


def action(project: Project, props: Props) -> Result:
    fs = project.filesystem

    # Folder
    path = props.path
    if props.folder:
        folder = fs.get_fullpath(props.folder)
        if not folder.exists():
            raise FrictionlessException("folder does not exist")
        path = str(folder / path)

    # Create
    path = helpers.write_file(project, path=path, bytes=props.bytes)

    return Result(path=path)
