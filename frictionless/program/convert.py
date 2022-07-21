import typer
from .main import program
from ..checklist import Checklist
from ..dialect import Dialect
from ..inquiry import Inquiry
from ..package import Package
from ..pipeline import Pipeline
from ..resource import Resource
from ..report import Report
from ..schema import Schema
from ..detector import Detector
from . import common


@program.command(name="convert")
def program_convert(
    # Source
    source: str = common.source,
    path: str = common.output_file_path,
    # Command
    json: bool = common.json,
    yaml: bool = common.yaml,
    er_diagram: bool = common.er_diagram,
    markdown: bool = common.markdown,
):
    """Convert metadata to various output"""

    # Validate input
    if not source:
        message = 'Providing "source" is required'
        typer.secho(message, err=True, fg=typer.colors.RED, bold=True)
        raise typer.Exit(1)

    metadata_type = Detector.detect_descriptor(source)
    if not metadata_type:
        message = "File not found"
        typer.secho(message, err=True, fg=typer.colors.RED, bold=True)
        raise typer.Exit(1)

    # Initialize metadata
    try:
        if metadata_type == "package":
            metadata = Package.from_descriptor(source)
        elif metadata_type == "resource":
            metadata = Resource.from_descriptor(source)
        elif metadata_type == "schema":
            metadata = Schema.from_descriptor(source)
        elif metadata_type == "checklist":
            metadata = Checklist.from_descriptor(source)
        elif metadata_type == "dialect":
            metadata = Dialect.from_descriptor(source)
        elif metadata_type == "report":
            metadata = Report.from_descriptor(source)
        elif metadata_type == "inquiry":
            metadata = Inquiry.from_descriptor(source)
        elif metadata_type == "detector":
            metadata = Detector.from_descriptor(source)
        elif metadata_type == "pipeline":
            metadata = Pipeline.from_descriptor(source)
    except Exception as exception:
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        raise typer.Exit(1)

    # Return json
    if json:
        content = metadata.to_json(path)
        typer.secho(content)
        raise typer.Exit()

    # Return yaml
    if yaml:
        content = metadata.to_yaml(path)
        typer.secho(content)
        raise typer.Exit()

    # Return ER Diagram
    if er_diagram:
        if metadata_type == "package":
            content = metadata.to_er_diagram(path)
            typer.secho(content)
            raise typer.Exit()
        else:
            message = "This feature is only available for package"
            typer.secho(message, err=True, fg=typer.colors.RED, bold=True)
            raise typer.Exit(1)

    # Return markdown
    if markdown:
        content = metadata.to_markdown(path)
        typer.secho(content)
        raise typer.Exit()

    # Return retcode
    message = "No target specified. For example --yaml"
    typer.secho(message, err=True, fg=typer.colors.RED, bold=True)
    raise typer.Exit(1)
