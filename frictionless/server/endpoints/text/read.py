from __future__ import annotations
from pydantic import BaseModel
from fastapi import Request
from ...project import Project
from ...router import router
from ... import helpers


# TODO: use detected resource.encoding if indexed


class Props(BaseModel):
    path: str


class Result(BaseModel):
    text: str


@router.post("/text/read")
def server_text_read(request: Request, props: Props) -> Result:
    return action(request.app.get_project(), props)


def action(project: Project, props: Props) -> Result:
    text = helpers.read_text(project, path=props.path)
    return Result(text=text)
