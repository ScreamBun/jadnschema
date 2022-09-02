from ..definitionBase import DefinitionBase


class Boolean(DefinitionBase):
    """
    An element with one of two values: true or false.
    """
    __root__: bool

    class Config:
        arbitrary_types_allowed = True

    class Options:
        data_type = "Boolean"
