from ..package import Package
from ..resource import Resource
from .package import transform_package
from .resource import transform_resource
from .pipeline import transform_pipeline


# TODO: sync with DEVT
# TODO: add source_type
# TODO: rename source_type -> type?
# TODO: handle source_type not found error
def transform(source, **options):
    """Transform resource

    API      | Usage
    -------- | --------
    Public   | `from frictionless import transform`

    Parameters:
        source (any): data source
    """
    if isinstance(source, Resource):
        return transform_resource(source, **options)
    elif isinstance(source, Package):
        return transform_package(source, **options)
    return transform_pipeline(source)
