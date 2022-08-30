from pydantic import ValidationError, root_validator
from .utils import validate_format
from ..definitionBase import DefinitionBase


class String(DefinitionBase):
    """
    A sequence of characters, each of which has a Unicode codepoint. Length is the number of characters.
    """
    __root__: str

    # Validation
    @root_validator(pre=True)
    def validate(cls, val: str):
        if fmt := cls.__options__.format:
            validate_format(cls, fmt, val)
        val_len = len(val)
        min_len = cls.__options__.minv or 0
        max_len = cls.__options__.maxv or 255
        if min_len > val_len:
            raise ValidationError(f"{cls.name} is invalid, minimum length of {min_len:,} characters not met")
        elif max_len < val_len:
            raise ValidationError(f"{cls.name} is invalid, maximum length of {min_len:,} characters exceeded")
        return val

    class Config:
        arbitrary_types_allowed = True
