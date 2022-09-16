"""
JADN Structure Types
"""
from enum import Enum, EnumMeta
from typing import ClassVar, Union
from pydantic import Extra, ValidationError, root_validator
from .definitionBase import DefinitionBase, DefinitionMeta


class Array(DefinitionBase):
    """
    An ordered list of labeled fields with positionally-defined semantics.
    Each field has a position, label, and type.
    """
    # __root__: Union[set, str, tuple]

    class Options:
        data_type = "Array"


class ArrayOf(DefinitionBase):
    """
    A collection of fields with the same semantics.
    Each field has type vtype.
    Ordering and uniqueness are specified by a collection option.
    """
    __root__: Union[set, str, tuple]

    class Options:
        data_type = "ArrayOf"


class Choice(DefinitionBase):
    """
    A discriminated union: one type selected from a set of named or labeled types.
    """
    # __root__: dict

    class Options:
        data_type = "Choice"


class EnumeratedMeta(DefinitionMeta):
    def __new__(mcs, name, bases, attrs, **kwargs):  # pylint: disable=bad-classmethod-argument
        base_enums = list(filter(None, [
            *[getattr(b, "__enums__", None) for b in reversed(bases) if issubclass(b, DefinitionBase) and b != DefinitionBase],
            attrs.pop("__enums__", None), attrs.pop("Values", None),
            kwargs.pop("__enums__", None), kwargs.pop("Values", None),
            getattr(mcs, "__enums__", None), getattr(mcs, "Values", None),
        ]))
        enums = {}
        for enum in base_enums:
            if isinstance(enum, (Enum, EnumMeta)):
                enums.update({e.name: e.value for e in enum})
            else:
                enums.update({k: getattr(enum, k) for k in vars(enum) if not k.startswith("_")})
        new_namespace = {
            **attrs,
            "__enums__": Enum(name, enums)
        }
        return super().__new__(mcs, name, bases, new_namespace, **kwargs)


class Enumerated(DefinitionBase, metaclass=EnumeratedMeta):  # pylint: disable=invalid-metaclass
    """
    A vocabulary of items where each item has an id and a string value.
    """
    __root__: Union[int, str]
    __enums__: ClassVar[Enum]

    # Pydantic overrides
    @classmethod
    def schema(cls) -> list:
        mro = [c for c in cls.__mro__ if not c.__name__ == cls.__name__][0]
        return [cls.name, mro.__name__, cls.__options__.schema(), (cls.__doc__ or "").strip(),
                [[v.value.extra["id"], v.value.default, v.value.description or ""] for v in cls.__enums__]]

    # Validation
    @root_validator(pre=True)
    def validate(cls, val: Union[int, str]):  # pylint: disable=no-self-argument
        if isinstance(val, int):
            for v in cls.__enums__:
                if val == v.value.extra.get("id", None):
                    return val
        else:
            for v in cls.__enums__:
                if val == v.name:
                    return val

        raise ValidationError(f"Value is not a valid for {cls.name}")

    class Options:
        data_type = "Enumerated"


class Map(DefinitionBase):
    """
    An unordered map from a set of specified keys to values with semantics bound to each key.
    Each key has an id and name or label, and is mapped to a value type.
    """
    # __root__: dict

    class Config:
        extra = Extra.allow

    class Options:
        data_type = "Map"
        minv = 1


class MapOf(DefinitionBase):
    """
    An unordered map from a set of keys of the same type to values with the same semantics.
    Each key has key type ktype, and is mapped to value type vtype.
    """
    # __root__: dict

    class Config:
        extra = Extra.allow

    class Options:
        data_type = "MapOf"


class Record(DefinitionBase):
    """
    An ordered map from a list of keys with positions to values with positionally-defined semantics.
    Each key has a position and name, and is mapped to a value type. Represents a row in a spreadsheet or database table.
    """
    # __root__: dict

    class Options:
        data_type = "Record"


__all__ = [
    "Array",
    "ArrayOf",
    "Choice",
    "Enumerated",
    "Map",
    "MapOf",
    "Record"
]
