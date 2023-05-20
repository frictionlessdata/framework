from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel
from fastapi import Request
from ....resources import JsonResource
from ...project import Project
from ...router import router


class Props(BaseModel):
    path: str
    data: Any
    deduplicate: Optional[bool] = None


class Result(BaseModel):
    path: str


@router.post("/json/write")
def endpoint(request: Request, props: Props) -> Result:
    return action(request.app.get_project(), props)


# TODO: delete report
def action(project: Project, props: Props) -> Result:
    fs = project.filesystem

    # Write
    target = fs.get_fullpath(props.path, deduplicate=props.deduplicate)
    resource = JsonResource(data=props.data)
    resource.write_json(path=str(target))
    path = fs.get_path(target)

    return Result(path=path)
