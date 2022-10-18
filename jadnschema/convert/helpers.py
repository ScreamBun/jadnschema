"""
Converter helpers
"""
from typing import Callable, Literal, Union
from .enums import CommentLevels, SchemaFormats
from ..utils import FrozenDict
__all__ = [
    # Helpers & Decorators
    "register", "register_reader", "register_writer",
    # Dynamic functions
    "dump", "dumps", "load", "loads"
]

registered = FrozenDict(
    reader=FrozenDict(),
    writer=FrozenDict()
)


# Helper
def register(rw: Literal["reader", "writer"], fmt: Union[str, Callable] = None, override: bool = False) -> Callable:
    """
    Decorator for a class to register it as a JADN converter
    :param rw: register as a reader or writer
    :param fmt: format of the converter
    :param override: override if there is an existing converter
    :return: return the original wrapped class after registration
    """
    def wrapper(cls: Callable, fmt: str = fmt, override: bool = override) -> Callable:
        global registered  # pylint: disable=global-statement
        regs = registered.unfreeze()

        regCls = regs[rw].get(fmt, None)
        if not hasattr(cls, "format"):
            raise AttributeError(f"{cls.__name__} requires attribute 'format'")

        if regCls and (regCls is not cls and not override):
            raise TypeError(f"{rw.title()} of type {fmt} has an implementation")

        regs[rw][fmt] = cls
        registered = FrozenDict(regs)
        return cls

    return wrapper if isinstance(fmt, str) else wrapper(fmt, fmt=getattr(fmt, "format", None))


def register_reader(fmt: Union[str, Callable] = None, override: bool = False) -> Callable:
    """
    Decorator for a class to register it as a conversion reader
    :param fmt: format of the converter
    :param override: override if there is an existing converter
    :return: return the original wrapped class after registration
    """
    return register("reader", fmt, override)


def register_writer(fmt: Union[str, Callable] = None, override: bool = False) -> Callable:
    """
    Decorator for a class to register it as a conversion writer
    :param fmt: format of the converter
    :param override: override if there is an existing converter
    :return: return the original wrapped class after registration
    """
    return register("writer", fmt, override)


# Dynamic
def dump(schema: Union[str, dict], fname: str, source: str = "", comm: str = CommentLevels.ALL, fmt: SchemaFormats = SchemaFormats.JADN, **kwargs):
    """
    Produce formatted schema from JADN schema
    :param schema: JADN Schema to convert
    :param fname: file to output
    :param source: name of original schema file
    :param comm: Level of comments to include in converted schema
    :param fmt: format of the desired output schema
    :return: None
    """
    cls = registered["writer"].get(fmt, None)
    if cls:
        comm = comm if comm in CommentLevels else CommentLevels.ALL
        return cls(schema, comm).dump(fname, source, **kwargs)

    raise ReferenceError(f"The format specified is not a known format - {fmt}")


def dumps(schema: Union[str, dict], comm: str = CommentLevels.ALL, fmt: SchemaFormats = SchemaFormats.JADN, **kwargs):
    """
    Produce formatted schema from JADN schema
    :param schema: JADN Schema to convert
    :param comm: Level of comments to include in converted schema
    :param fmt: format of the desired output schema
    :return: formatted schema
    """
    cls = registered["writer"].get(fmt, None)
    if cls:
        comm = comm if comm in CommentLevels else CommentLevels.ALL
        return cls(schema, comm).dumps(**kwargs)

    raise ReferenceError(f"The format specified is not a known format - {fmt}")


def load(schema: Union[str, dict], source: str = "", fmt: SchemaFormats = SchemaFormats.JADN, **kwargs):
    """
    Produce JADN schema from input schema
    :param schema: Schema to convert
    :param source: name of original schema file
    :param fmt: format of the input schema
    :return: loaded JADN schema
    """
    if cls := registered["reader"].get(fmt, None):
        return cls().load(schema, source, **kwargs)

    raise ReferenceError(f"The format specified is not a known format - {fmt}")


def loads(schema: Union[str, dict], fmt: SchemaFormats = SchemaFormats.JADN, **kwargs):
    """
    Produce JADN schema from input schema
    :param schema: schema file to convert
    :param fmt: format of the input schema
    :return: loaded JADN schema
    """
    if cls := registered["reader"].get(fmt, None):
        return cls().loads(schema, **kwargs)

    raise ReferenceError(f"The format specified is not a known format - {fmt}")
