from pydantic import ValidationError, root_validator
from ..definitionBase import DefinitionBase


class Number(DefinitionBase):
    """
    A real number.
    """
    __root__: float

    # Validation
    @root_validator(pre=True)
    def validate(cls, val: int):  # pylint: disable=no-self-argument
        min_val = cls.__options__.minf or 0
        max_val = cls.__options__.maxf or 0

        if min_val > val:
            raise ValidationError(f"{cls.name} is invalid, minimum of {min_val:,} not met")
        if max_val != 0 and max_val < val:
            raise ValidationError(f"{cls.name} is invalid, maximum of {max_val:,} exceeded")
        return val

    class Config:
        arbitrary_types_allowed = True

    class Options:
        data_type = "Number"
