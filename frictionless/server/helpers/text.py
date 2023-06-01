from __future__ import annotations
from typing import TYPE_CHECKING
from ...resources import TextResource

if TYPE_CHECKING:
    from ..project import Project


def read_text(project: Project, *, path: str):
    fs = project.filesystem

    fullpath = fs.get_fullpath(path)
    resource = TextResource(path=str(fullpath))
    text = resource.read_text()

    return text


def write_text(project: Project, *, path: str, text: str):
    fs = project.filesystem

    fullpath = fs.get_fullpath(path)
    resource = TextResource(data=text)
    resource.write_text(path=str(fullpath))
    path = fs.get_path(fullpath)

    return path
