from __future__ import annotations
from tinydb import Query
from pydantic import BaseModel
from fastapi import Request
from ...project import Project
from ...router import router
from ... import types


class Props(BaseModel):
    chart: types.IChart


class Result(BaseModel):
    chart: types.IChart


@router.post("/chart/render")
def endpoint(request: Request, props: Props) -> Result:
    return action(request.app.get_project(), props)


# TODO: review/rewrite
def action(project: Project, props: Props) -> Result:
    md = project.metadata
    db = project.database

    chart = props.chart.copy()
    path = chart.get("data", {}).pop("url", None)
    if not path:
        return Result(chart=chart)
    descriptor = md.find_document(type="record", query=Query().path == path)
    if not descriptor:
        return Result(chart=chart)
    name = descriptor["name"]
    if not name:
        return Result(chart=chart)
    # TODO: cherry-pick fields based on presense in the chart
    result = db.query(f'SELECT * from "{name}"')
    # TODO: check if some data types need to be stringified
    # TODO: fix
    chart["data"]["values"] = result["rows"]  # type: ignore

    return Result(chart=chart)
