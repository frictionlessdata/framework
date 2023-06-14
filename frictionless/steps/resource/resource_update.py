from __future__ import annotations
import attrs
from copy import deepcopy
from typing import TYPE_CHECKING, Optional
from ...exception import FrictionlessException
from ...pipeline import Step
from ... import helpers
from ... import errors

if TYPE_CHECKING:
    from ...package import Package
    from ...resource import Resource
    from ... import types


@attrs.define(kw_only=True, repr=False)
class resource_update(Step):
    """Update resource.

    This step can be added using the `steps` parameter
    for the `transform` function.

    """

    type = "resource-update"

    name: Optional[str] = None
    """
    Name of the resource to update.
    """

    descriptor: types.IDescriptor
    """
    New descriptor for the resource to update metadata.
    """

    # Transform

    def transform_package(self, package: Package):
        if not self.name:
            note = 'Property "name" is required for "resource_update" within a package'
            raise FrictionlessException(errors.StepError(note=note))
        descriptor = deepcopy(self.descriptor)
        package.update_resource(self.name, descriptor)

    # NOTE: This implementation is not type safe
    # Consider moving away from descriptor to named/typed properties
    def transform_resource(self, resource: Resource):
        options = helpers.create_options(self.descriptor)
        for name, value in options.items():
            setattr(resource, name, value)

    # Metadata

    metadata_profile_patch = {
        "required": ["descriptor"],
        "properties": {
            "name": {"type": "string"},
            "descriptor": {"type": "object"},
        },
    }
