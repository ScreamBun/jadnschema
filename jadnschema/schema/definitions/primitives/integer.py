from ..definitionBase import DefinitionBase


class Integer(DefinitionBase):
    """
    A positive or negative whole number.
    """
    __root__: int

    class Config:
        arbitrary_types_allowed = True
