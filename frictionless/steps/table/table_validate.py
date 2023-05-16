from __future__ import annotations
import attrs
from typing import TYPE_CHECKING
from ...pipeline import Step
from ...exception import FrictionlessException

if TYPE_CHECKING:
    from ...resource import Resource


@attrs.define(kw_only=True)
class table_validate(Step):
    """Validate table.

    This step can be added using the `steps` parameter
    for the `transform` function.

    """

    type = "table-validate"

    # Transform

    def transform_resource(self, resource: Resource):
        current = resource.to_copy()

        # Data
        def data():  # type: ignore
            with current:
                if not current.header.valid:  # type: ignore
                    raise FrictionlessException(error=current.header.errors[0])  # type: ignore
                yield current.header  # type: ignore
                for row in current.row_stream:  # type: ignore
                    if not row.valid:  # type: ignore
                        raise FrictionlessException(error=row.errors[0])  # type: ignore
                    yield row

        # Meta
        resource.data = data
