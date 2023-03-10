from __future__ import annotations
import os
import typer
from typing import List
from rich.console import Console
from ..resource import Resource
from .program import program
from ..system import system
from . import common
from . import utils


@program.command(name="explore")
def program_explore(
    # Resource
    source: List[str] = common.source,
    name: str = common.resource_name,
    type: str = common.type,
    path: str = common.path,
    # System
    debug: bool = common.debug,
    trusted: bool = common.trusted,
    standards: str = common.standards,
):
    """Script data"""
    console = Console()

    # Setup system
    if trusted:
        system.trusted = trusted
    if standards:
        system.standards = standards  # type: ignore

    # Create source
    source = utils.create_source(source, path=path)
    if not source and not path:
        note = 'Providing "source" or "path" is required'
        utils.print_error(console, note=note)
        raise typer.Exit(code=1)

    # Get paths
    try:
        resource = Resource(
            source=utils.create_source(source),
            name=name,
            path=path,
            datatype=type or "",
        )
        resources = resource.list()
        paths = [resource.normpath for resource in resources if resource.normpath]
    except Exception as exception:
        utils.print_exception(console, debug=debug, exception=exception)
        raise typer.Exit(code=1)

    # Enter editor
    os.system(f"vd {' '.join(paths)}")
