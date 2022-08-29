from ..definitionBase import DefinitionBase


class Number(DefinitionBase):
    """
    A real number.
    """
    __root__: float

    class Config:
        arbitrary_types_allowed = True
