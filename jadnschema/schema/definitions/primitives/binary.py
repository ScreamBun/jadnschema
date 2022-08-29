from ..definitionBase import DefinitionBase


class Binary(DefinitionBase):
    """
    A sequence of octets. Length is the number of octets.
    """
    __root__: str

    class Config:
        arbitrary_types_allowed = True
