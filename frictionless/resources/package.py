from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from ..exception import FrictionlessException
from ..report import Report
from ..package import Package
from .metadata import MetadataResource
from .. import settings

if TYPE_CHECKING:
    from ..checklist import Checklist
    from ..interfaces import ICallbackFunction
    from ..interfaces import IFilterFunction, IProcessFunction, IExtractedRows


class PackageResource(MetadataResource):
    datatype = "package"

    # Read

    def read_package(self) -> Package:
        return Package.from_descriptor(self.descriptor, basepath=self.basepath)

    # Extract

    def extract(
        self,
        *,
        name: Optional[str] = None,
        filter: Optional[IFilterFunction] = None,
        process: Optional[IProcessFunction] = None,
        limit_rows: Optional[int] = None,
    ) -> IExtractedRows:
        package = self.read_package()
        return package.extract(
            name=name, filter=filter, process=process, limit_rows=limit_rows
        )

    # Validate

    def validate(
        self,
        checklist: Optional[Checklist] = None,
        *,
        limit_errors: int = settings.DEFAULT_LIMIT_ERRORS,
        limit_rows: Optional[int] = None,
        on_row: Optional[ICallbackFunction] = None,
    ) -> Report:
        try:
            package = self.read_package()
        except FrictionlessException as exception:
            return Report.from_validation(errors=exception.to_errors())
        return package.validate(
            checklist, limit_errors=limit_errors, limit_rows=limit_rows
        )
