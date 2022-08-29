from ..definitionBase import DefinitionBase


class Record(DefinitionBase):
    """
    An ordered map from a list of keys with positions to values with positionally-defined semantics
    Each key has a position and name, and is mapped to a value type. Represents a row in a spreadsheet or database table
    """
    # __root__: dict
