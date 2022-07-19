from __future__ import annotations
from ...plugin import Plugin
from ... import helpers
from .control import BigqueryControl
from .parser import BigqueryParser
from .storage import BigqueryStorage


# NOTE:
# We need to ensure that the way we detect bigquery service is good enough.
# We don't want to be importing google and checking the type withouth a good reason


class BigqueryPlugin(Plugin):
    """Plugin for BigQuery"""

    # Hooks

    def create_control(self, descriptor):
        if descriptor.get("type") == "bigquery":
            return BigqueryControl.from_descriptor(descriptor)

    def create_parser(self, resource):
        if resource.format == "bigquery":
            return BigqueryParser(resource)

    def create_storage(self, name, source, **options):
        if name == "bigquery":
            return BigqueryStorage(source, **options)

    def detect_resource(self, resource):
        if not resource.scheme and not resource.format and resource.memory:
            if helpers.is_type(resource.data, "Resource"):
                resource.type = "table"
                resource.scheme = ""
                resource.format = "bigquery"