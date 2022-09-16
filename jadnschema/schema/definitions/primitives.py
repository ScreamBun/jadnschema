"""
JADN Primitive Types
"""
import re

from functools import partial
from typing import Union
from pydantic import ValidationError, root_validator
from .definitionBase import DefinitionBase
Primitive = Union["Binary", "Boolean", "Integer", "Number", "String"]


def validate_format(cls: Primitive, fmt: str, val: str) -> str:
    if re.match(r"^u\d+$", fmt):
        fun = partial(cls.__options__.validation["unsigned"], int(fmt[1:]))
    else:
        fun = cls.__options__.validation.get(fmt, None)

    if fun:
        return fun(val)
    return val


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


class Boolean(DefinitionBase):
    """
    An element with one of two values: true or false.
    """
    __root__: bool

    class Config:
        arbitrary_types_allowed = True

    class Options:
        data_type = "Boolean"


class Integer(DefinitionBase):
    """
    A positive or negative whole number.
    """
    __root__: int

    # Validation
    @root_validator(pre=True)
    def validate(cls, val: int):  # pylint: disable=no-self-argument
        if fmt := cls.__options__.format:
            validate_format(cls, fmt, str(val))
        min_val = cls.__options__.minv or 0
        max_val = cls.__options__.maxv or 0

        if min_val > val:
            raise ValidationError(f"{cls.name} is invalid, minimum of {min_val:,} not met")
        if max_val != 0 and max_val < val:
            raise ValidationError(f"{cls.name} is invalid, maximum of {max_val:,} exceeded")
        return val

    class Config:
        arbitrary_types_allowed = True

    class Options:
        data_type = "Integer"


class Number(DefinitionBase):
    """
    A real number.
    """
    __root__: float

    # Validation
    @root_validator(pre=True)
    def validate(cls, val: int):  # pylint: disable=no-self-argument
        if fmt := cls.__options__.format:
            validate_format(cls, fmt, str(val))
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


class String(DefinitionBase):
    """
    A sequence of characters, each of which has a Unicode codepoint. Length is the number of characters.
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
            raise ValidationError(f"{cls.name} is invalid, minimum length of {min_len:,} characters not met")
        if max_len < val_len:
            raise ValidationError(f"{cls.name} is invalid, maximum length of {min_len:,} characters exceeded")
        return val

    class Config:
        arbitrary_types_allowed = True

    class Options:
        data_type = "String"


__all__ = [
    "Primitive",
    "Binary",
    "Boolean",
    "Integer",
    "Number",
    "String"
]
