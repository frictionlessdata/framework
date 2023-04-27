from pydantic import BaseModel
from typing import Optional
from fastapi import Request
from ...project import Project, IChart
from ...router import router
from .. import json


class Props(BaseModel):
    path: Optional[str]
    chart: Optional[IChart]


class Result(BaseModel):
    path: str


@router.post("/chart/create")
def endpoint(request: Request, props: Props) -> Result:
    return action(request.app.get_project(), props)


def action(project: Project, props: Props) -> Result:
    path = props.path or "chart.json"
    data = props.chart or {"encoding": {}}
    result = json.write.action(
        project, json.write.Props(path=path, data=data, deduplicate=True)
    )
    return Result(path=result.path)
