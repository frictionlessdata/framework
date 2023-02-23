from __future__ import annotations
from typing import TYPE_CHECKING
from ...system import Plugin
from .control import SpssControl
from .parser import SpssParser

if TYPE_CHECKING:
    from ...resource import Resource


class SpssPlugin(Plugin):
    """Plugin for SPSS"""

    # Hooks

    def create_parser(self, resource):
        if resource.format in ["sav", "zsav"]:
            return SpssParser(resource)

    def detect_resource_type(self, resource: Resource):
        if resource.format in ["sav", "zsav"]:
            return "table"

    def select_Control(self, type):
        if type == "spss":
            return SpssControl
