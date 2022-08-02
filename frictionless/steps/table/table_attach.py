from __future__ import annotations
import attrs
from typing import Union
from ...pipeline import Step
from ...platform import platform
from ...resource import Resource


@attrs.define(kw_only=True)
class table_attach(Step):
    """Attach table"""

    type = "table-attach"

    # State

    resource: Union[Resource, str]
    """NOTE: add docs
    """

    # Transform

    def transform_resource(self, resource):
        source = self.resource
        target = resource
        if isinstance(source, str):
            assert target.package
            source = target.package.get_resource(source)
        source.infer()
        view1 = target.to_petl()
        view2 = source.to_petl()
        for field in source.schema.fields:
            target.schema.fields.append(field.to_copy())
        resource.data = platform.petl.annex(view1, view2)

    # Metadata

    metadata_Types = dict(resource=Resource)
    metadata_profile_patch = {
        "required": ["resource"],
        "properties": {
            "resource": {"type": ["object", "string"]},
        },
    }
