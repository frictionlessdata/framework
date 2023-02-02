from typing import Optional
from pydantic import BaseModel
from fastapi import Request
from ...project import Project, IResourceItem
from ..router import router


class Props(BaseModel):
    session: Optional[str]
    path: str


class Result(BaseModel):
    item: IResourceItem


@router.post("/resource/create")
def server_resource_create(request: Request, props: Props) -> Result:
    project: Project = request.app.get_project(props.session)
    item = project.resource_create(props.path)
    return Result(item=item)
