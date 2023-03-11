from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List
from ..exception import FrictionlessException
from ..report import Report
from ..resource import Resource
from .metadata import MetadataResource
from .. import settings

if TYPE_CHECKING:
    from ..pipeline import Pipeline
    from ..checklist import Checklist
    from ..interfaces import ICallbackFunction
    from ..interfaces import IFilterFunction, IProcessFunction, ITabularData


class ResourceResource(MetadataResource[Resource]):
    datatype = "resource"
    dataclass = Resource

    # Extract

    def extract(
        self,
        *,
        name: Optional[str] = None,
        filter: Optional[IFilterFunction] = None,
        process: Optional[IProcessFunction] = None,
        limit_rows: Optional[int] = None,
    ) -> ITabularData:
        resource = self.read_metadata()
        return resource.extract(
            name=name, filter=filter, process=process, limit_rows=limit_rows
        )

    # Index

    def index(self, database_url: str, **options) -> List[str]:
        resource = self.read_metadata()
        return resource.index(database_url, **options)

    # List

    def list(self, *, name: Optional[str] = None) -> List[Resource]:
        """List dataset resources"""
        resource = self.read_metadata()
        return [resource]

    # Validate

    def validate(
        self,
        checklist: Optional[Checklist] = None,
        *,
        name: Optional[str] = None,
        on_row: Optional[ICallbackFunction] = None,
        parallel: bool = False,
        limit_rows: Optional[int] = None,
        limit_errors: int = settings.DEFAULT_LIMIT_ERRORS,
    ) -> Report:
        try:
            resource = self.read_metadata()
        except FrictionlessException as exception:
            return Report.from_validation(errors=exception.to_errors())
        return resource.validate(
            checklist, limit_errors=limit_errors, limit_rows=limit_rows, on_row=on_row
        )

    # Transform

    def transform(self, pipeline: Pipeline):
        resource = self.read_metadata()
        return resource.transform(pipeline)
