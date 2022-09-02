from pydantic import Extra
from ..definitionBase import DefinitionBase


class Map(DefinitionBase):
    """
    An unordered map from a set of specified keys to values with semantics bound to each key
    Each key has an id and name or label, and is mapped to a value type
    """
    # __root__: dict

    class Config:
        extra = Extra.allow

    class Options:
        data_type = "Map"
        minv = 1
