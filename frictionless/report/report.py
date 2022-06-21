from __future__ import annotations
import functools
import textwrap
from copy import deepcopy
from importlib import import_module
from tabulate import tabulate
from typing import TYPE_CHECKING, Optional, List
from ..metadata2 import Metadata2
from ..errors import Error, ReportError
from ..exception import FrictionlessException
from .validate import validate
from .. import settings
from .. import helpers

if TYPE_CHECKING:
    from ..resource import Resource


class Report(Metadata2):
    """Report representation."""

    validate = validate

    def __init__(
        self,
        *,
        version: str,
        valid: bool,
        stats: dict,
        tasks: List[ReportTask] = [],
        errors: List[Error] = [],
        warnings: List[str] = [],
    ):
        self.version = version
        self.valid = valid
        self.stats = stats
        self.tasks = tasks.copy()
        self.errors = errors.copy()
        self.warnings = warnings.copy()

    # Properties

    version: str
    """# TODO: add docs"""

    valid: bool
    """# TODO: add docs"""

    stats: dict
    """# TODO: add docs"""

    tasks: List[ReportTask]
    """# TODO: add docs"""

    errors: List[Error]
    """# TODO: add docs"""

    warnings: List[str]
    """# TODO: add docs"""

    @property
    def task(self):
        """
        Returns:
            ReportTask: validation task (if there is only one)

        Raises:
            FrictionlessException: if there are more that 1 task
        """
        if len(self.tasks) != 1:
            error = Error(note='The "report.task" is available for single task reports')
            raise FrictionlessException(error)
        return self.tasks[0]

    # Flatten

    def flatten(self, spec=["taskPosition", "rowPosition", "fieldPosition", "code"]):
        """Flatten the report

        Parameters
            spec (any[]): flatten specification

        Returns:
            any[]: flatten report
        """
        result = []
        for error in self.errors:
            context = {}
            context.update(error)
            result.append([context.get(prop) for prop in spec])
        for count, task in enumerate(self.tasks, start=1):
            for error in task.errors:
                context = {"taskNumber": count, "taskPosition": count}
                context.update(error)
                result.append([context.get(prop) for prop in spec])
        return result

    # Convert

    @staticmethod
    def from_validation(
        *,
        time: float,
        tasks: List[ReportTask] = [],
        errors: List[Error] = [],
        warnings: List[str] = [],
    ):
        """Create a report from a validation"""
        tasks = tasks.copy()
        errors = errors.copy()
        warnings = warnings.copy()
        error_count = len(errors) + sum(task.stats["errors"] for task in tasks)
        stats = {"time": time, "tasks": len(tasks), "errors": error_count}
        return Report(
            version=settings.VERSION,
            valid=not error_count,
            stats=stats,
            tasks=tasks,
            errors=errors,
            warnings=warnings,
        )

    @staticmethod
    def from_validation_task(
        resource: Resource,
        *,
        time: float,
        scope: List[str] = [],
        errors: List[Error] = [],
        warnings: List[str] = [],
    ):
        """Create a report from a validation task"""
        scope = scope.copy()
        errors = errors.copy()
        warnings = warnings.copy()
        task_stats = helpers.copy_merge(resource.stats, time=time, errors=len(errors))
        report_stats = {"time": time, "tasks": 1, "errors": len(errors)}
        return Report(
            version=settings.VERSION,
            valid=not errors,
            stats=report_stats,
            errors=[],
            tasks=[
                ReportTask(
                    valid=not errors,
                    name=resource.name,  # type: ignore
                    place=resource.place,  # type: ignore
                    tabular=resource.tabular,  # type: ignore
                    stats=task_stats,
                    scope=scope,
                    errors=errors,
                    warnings=warnings,
                )
            ],
        )

    @staticmethod
    def from_validation_reports(
        *,
        time: float,
        reports: List[Report],
    ):
        """Create a report from a set of validation reports"""
        tasks = []
        errors = []
        warnings = []
        for report in reports:
            tasks.extend(report.tasks)
            errors.extend(report.errors)
            warnings.extend(report.warnings)
        return Report.from_validation(
            time=time,
            tasks=tasks,
            errors=errors,
            warnings=warnings,
        )

    # TODO: move to ReportTask
    def to_summary(self):
        """Summary of the report

        Returns:
            str: validation report
        """

        validation_content = ""
        for task in self.tasks:
            prefix = "valid" if task.valid else "invalid"
            suffix = "" if task.tabular else "(non-tabular)"
            validation_content += f"\n# {'-'*len(prefix)}"
            validation_content += f"\n# {prefix}: {task.place} {suffix}"
            validation_content += f"\n# {'-'*len(prefix)}"
            error_content = []
            if task.errors:
                for error in task.errors:
                    error_content.append(
                        [
                            error.get("rowPosition", ""),
                            error.get("fieldPosition", ""),
                            error.code,
                            error.message,
                        ]
                    )
            # Validate
            error_content = helpers.wrap_text_to_colwidths(error_content)
            validation_content += "\n\n"
            validation_content += "## Summary "
            validation_content += "\n\n"
            validation_content += task.to_summary()
            validation_content += "\n\n"
            # errors
            if task.errors:
                validation_content += "## Errors "
                validation_content += "\n\n"
                validation_content += str(
                    tabulate(
                        error_content,
                        headers=["row", "field", "code", "message"],
                        tablefmt="grid",
                    )
                )
                validation_content += "\n\n"
        return validation_content

    # Metadata

    metadata_Error = ReportError
    metadata_profile = {
        "properties": {
            "version": {},
            "valid": {},
            "stats": {},
            "tasks": {},
            "errors": {},
            "warnings": {},
        }
    }

    # TODO: validate valid/errors count
    # TODO: validate stats when the class is added
    # TODO: validate errors when metadata is reworked
    def metadata_validate(self):
        yield from super().metadata_validate()

        # Tasks
        for task in self.tasks:
            yield from task.metadata_errors


class ReportTask(Metadata2):
    """Report task representation."""

    def __init__(
        self,
        *,
        valid: bool,
        name: str,
        place: str,
        tabular: bool,
        stats: dict,
        scope: Optional[List[str]] = None,
        warnings: Optional[List[str]] = None,
        errors: Optional[List[Error]] = None,
    ):
        self.valid = valid
        self.name = name
        self.place = place
        self.tabular = tabular
        self.stats = stats
        self.scope = scope or []
        self.warnings = warnings or []
        self.errors = errors or []

    # Properties

    valid: bool
    """# TODO: add docs"""

    name: str
    """# TODO: add docs"""

    place: str
    """# TODO: add docs"""

    tabular: bool
    """# TODO: add docs"""

    stats: dict
    """# TODO: add docs"""

    scope: List[str]
    """# TODO: add docs"""

    warnings: List[str]
    """# TODO: add docs"""

    errors: List[Error]
    """# TODO: add docs"""

    @property
    def error(self):
        """
        Returns:
            Error: validation error if there is only one

        Raises:
            FrictionlessException: if more than one errors
        """
        if len(self.errors) != 1:
            error = Error(note='The "task.error" is available for single error tasks')
            raise FrictionlessException(error)
        return self.errors[0]

    # Flatten

    def flatten(self, spec=["rowPosition", "fieldPosition", "code"]):
        """Flatten the report

        Parameters
            spec (any[]): flatten specification

        Returns:
            any[]: flatten task report
        """
        result = []
        for error in self.errors:
            context = {}
            context.update(error)
            result.append([context.get(prop) for prop in spec])
        return result

    # Convert

    def to_summary(self) -> str:
        """Generate summary for validation task"

        Returns:
            str: validation summary
        """
        error_list = {}
        for error in self.errors:
            error_title = f"{error.name} ({error.code})"
            if error_title not in error_list:
                error_list[error_title] = 0
            error_list[error_title] += 1
        content = [
            ["File place", self.place],
            ["File size", helpers.format_bytes(self.stats["bytes"])],
            ["Total Time", self.stats.get("time")],
            ["Rows Checked", self.stats.get("rows")],
        ]
        if error_list:
            content.append(["Total Errors", sum(error_list.values())])
        for code, count in error_list.items():
            content.append([code, count])
        output = ""
        for warning in self.warnings:
            output += f">> {warning}\n\n"
        output += tabulate(content, headers=["Name", "Value"], tablefmt="grid")
        return output

    # Metadata

    metadata_Error = ReportError
    metadata_profile = {
        "properties": {
            "valid": {},
            "name": {},
            "place": {},
            "tabular": {},
            "stats": {},
            "scope": {},
            "warnings": {},
            "errors": {},
        }
    }

    # TODO: validate valid/errors count
    # TODO: validate stats when the class is added
    # TODO: validate errors when metadata is reworked
    def metadata_validate(self):
        yield from super().metadata_validate()
