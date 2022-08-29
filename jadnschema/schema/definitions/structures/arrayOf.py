from typing import Union
from ..definitionBase import DefinitionBase


class ArrayOf(DefinitionBase):
    """
    A collection of fields with the same semantics
    Each field has type vtype
    Ordering and uniqueness are specified by a collection option
    """
    __root__: Union[set, str, tuple]
