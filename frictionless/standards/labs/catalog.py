from __future__ import annotations
from typing import List, Union
from typing_extensions import TypedDict, Required
from ..core import IPackage


class ICatalog(TypedDict, total=False):
    name: str
    type: str
    title: str
    description: str
    packages: Required[List[Union[IPackage, str]]]
