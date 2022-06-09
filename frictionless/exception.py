from __future__ import annotations
from typing import TYPE_CHECKING, Type, Union
from importlib import import_module

if TYPE_CHECKING:
    from .error import Error


class FrictionlessException(Exception):
    """Main Frictionless exception

    API      | Usage
    -------- | --------
    Public   | `from frictionless import FrictionlessException`

    Parameters:
        error (Error): an underlaying error

    """

    def __init__(self, error: Union[str, Error]):
        ErrorClass: Type[Error] = import_module("frictionless").Error
        self.__error = error if isinstance(error, Error) else ErrorClass(note=error)
        super().__init__(f"[{self.error.code}] {self.error.message}")

    @property
    def error(self) -> Error:
        """
        Returns:
            Error: error
        """
        return self.__error
