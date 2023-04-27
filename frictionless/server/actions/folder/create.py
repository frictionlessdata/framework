from typing import Optional
from pydantic import BaseModel
from fastapi import Request
from ...project import Project
from ...router import router
from .... import helpers


class Props(BaseModel):
    # TODO: rebase on path?
    name: str
    folder: Optional[str]


class Result(BaseModel):
    path: str


@router.post("/folder/create")
def endpoint(request: Request, props: Props) -> Result:
    return action(request.app.get_project(), props)


def action(project: Project, props: Props) -> Result:
    assert project.is_filename(props.name)
    folder = props.folder
    if folder:
        folder = project.get_secure_fullpath(folder)
        assert project.is_folder(folder)
    fullpath = project.get_secure_fullpath(folder, props.name, deduplicate=True)
    helpers.create_folder(fullpath)
    path = project.get_secure_relpath(fullpath)
    return Result(path=path)
