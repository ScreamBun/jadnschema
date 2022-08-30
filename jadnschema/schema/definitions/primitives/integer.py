from pydantic import ValidationError, root_validator
from .utils import validate_format
from ..definitionBase import DefinitionBase


class Integer(DefinitionBase):
    """
    A positive or negative whole number.
    """
    __root__: int

    # Validation
    @root_validator(pre=True)
    def validate(cls, val: int):
        if fmt := cls.__options__.format:
            validate_format(cls, fmt, str(val))
        min_val = cls.__options__.minv or 0
        max_val = cls.__options__.maxv or 0

        if min_val > val:
            raise ValidationError(f"{cls.name} is invalid, minimum of {min_val:,} not met")
        elif max_val != 0 and max_val < val:
            raise ValidationError(f"{cls.name} is invalid, maximum of {max_val:,} exceeded")
        return val

    class Config:
        arbitrary_types_allowed = True
