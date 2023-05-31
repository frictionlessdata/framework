from typing import Any, Optional, cast
from ..metadata import Metaclass
from ..platform import platform
from ..dialect import Control
from ..system import system
from .. import helpers


class Factory(Metaclass):
    def __call__(
        cls,
        source: Optional[Any] = None,
        *params: Any,
        control: Optional[Control] = None,
        basepath: Optional[str] = None,
        packagify: bool = True,
        **options: Any
    ):
        assert not params
        source = helpers.normalize_source(source)

        # Adapter
        if source is not None or control is not None:
            adapter = system.create_adapter(
                source,
                control=control,
                basepath=basepath,
                packagify=packagify,
            )
            if adapter:
                package = adapter.read_package()
                return package

        # Descriptor
        if source is not None:
            return cls.from_descriptor(source, basepath=basepath, **options)  # type: ignore

        # Default
        return cast(
            platform.frictionless.Package,
            type.__call__(cls, basepath=basepath, **options),
        )
