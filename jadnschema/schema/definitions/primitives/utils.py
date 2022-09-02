import re

from functools import partial
from typing import Type, Union

Primitive = Type[Union["Binary", "Boolean", "Integer", "Number", "String"]]


def validate_format(cls: Primitive, fmt: str, val: str) -> str:
    if re.match(r"^u\d+$", fmt):
        fun = partial(cls.__options__.validation["unsigned"], int(fmt[1:]))
    else:
        fun = cls.__options__.validation.get(fmt, None)

    if fun:
        return fun(val)
    return val
