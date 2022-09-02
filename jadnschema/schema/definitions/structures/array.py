from ..definitionBase import DefinitionBase


class Array(DefinitionBase):
    """
    An ordered list of labeled fields with positionally-defined semantics
    Each field has a position, label, and type
    """
    # __root__: Union[set, str, tuple]

    class Options:
        data_type = "Array"
