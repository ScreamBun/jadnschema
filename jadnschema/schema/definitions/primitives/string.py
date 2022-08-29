from ..definitionBase import DefinitionBase


class String(DefinitionBase):
    """
    A sequence of characters, each of which has a Unicode codepoint. Length is the number of characters.
    """
    __root__: str

    class Config:
        arbitrary_types_allowed = True
