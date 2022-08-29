from ..definitionBase import DefinitionBase


class MapOf(DefinitionBase):
    """
    An unordered map from a set of keys of the same type to values with the same semantics
    Each key has key type ktype, and is mapped to value type vtype
    """
    # __root__: dict
