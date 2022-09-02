from ..definitionBase import DefinitionBase


class Choice(DefinitionBase):
    """
    A discriminated union: one type selected from a set of named or labeled types
    """
    # __root__: dict

    class Options:
        data_type = "Choice"
