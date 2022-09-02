from pydantic import ValidationError, root_validator
from .utils import validate_format
from ..definitionBase import DefinitionBase


class Binary(DefinitionBase):
    """
    A sequence of octets. Length is the number of octets.
    """
    __root__: str

    # Validation
    @root_validator(pre=True)
    def validate(cls, val: str):  # pylint: disable=no-self-argument
        if fmt := cls.__options__.format:
            validate_format(cls, fmt, val)
        val_len = len(val)
        min_len = cls.__options__.minv or 0
        max_len = cls.__options__.maxv or 255
        if min_len > val_len:
            raise ValidationError(f"{cls.name} is invalid, minimum length of {min_len:,} bytes not met")
        if max_len < val_len:
            raise ValidationError(f"{cls.name} is invalid, maximum length of {min_len:,} bytes exceeded")
        return val

    class Config:
        arbitrary_types_allowed = True

    class Options:
        data_type = "Binary"
