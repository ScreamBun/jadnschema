from enum import Enum, EnumMeta
from typing import ClassVar, Union
from pydantic import ValidationError, root_validator
from ..definitionBase import DefinitionBase, DefinitionMeta


class EnumeratedMeta(DefinitionMeta):
    def __new__(mcs, name, bases, attrs, **kwargs):
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


class Enumerated(DefinitionBase, metaclass=EnumeratedMeta):
    """
    A vocabulary of items where each item has an id and a string value
    """
    __root__: Union[int, str]
    __enums__: ClassVar[Enum]

    # Pydantic overrides
    @classmethod
    def schema(cls) -> list:
        mro = [c for c in cls.__mro__ if not c.__name__ == cls.__name__][0]
        schema = [cls.name, mro.__name__, cls.__options__.schema(), (cls.__doc__ or "").strip()]
        schema.append([[v.value.extra.get("id"), v.value.default, v.value.description or ""] for v in cls.__enums__])
        return schema

    # Validation
    @root_validator(pre=True)
    def validate(cls, val: Union[int, str]):
        if isinstance(val, int):
            for v in cls.__enums__:
                if val == v.value.extra.get("id", None):
                    return val
        else:
            for v in cls.__enums__:
                if val == v.name:
                    return val

        raise ValidationError(f"Value is not a valid for {cls.name}")
