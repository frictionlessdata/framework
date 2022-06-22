from ...plugin import Plugin
from .control import CsvControl
from .parser import CsvParser


class CsvPlugin(Plugin):
    """Plugin for Pandas"""

    code = "csv"

    # Hooks

    def create_control(self, descriptor):
        if descriptor.get("code") == "csv":
            return CsvControl.from_descriptor(descriptor)

    def create_parser(self, resource):
        if resource.format in ["csv", "tsv"]:
            return CsvParser(resource)
