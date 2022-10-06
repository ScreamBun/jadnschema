import re

from collections import namedtuple
from enum import Enum
from typing import Callable, Dict, Type, Optional, Tuple, Union, get_args
from pydantic import Field, create_model  # pylint: disable=no-name-in-module
from pydantic.fields import FieldInfo  # pylint: disable=no-name-in-module
from ..consts import FieldAlias
from .options import Options
from .definitionBase import DefinitionBase
from .primitives import Binary, Boolean, Integer, Number, String
from .structures import Array, ArrayOf, Choice, Map, Enumerated, MapOf, Record

Primitive = Union[Binary, Boolean, Integer, Number, String]
Structure = Union[Array, ArrayOf, Choice, Enumerated, Map, MapOf, Record]
Definition = Union[Primitive, Structure]

jadn_def = namedtuple("jadn_def", ("name", "type", "options", "description", "fields"), defaults=(None, None, [], "", []))
def_field = namedtuple("def_field", ("id", "name", "type", "options", "description"))
enum_field = namedtuple("enum_field", ("id", "name", "description"))

DefTypes = {d.__name__: d for d in get_args(Definition)}

__all__ = [
    # Definitions
    "Binary",
    "Boolean",
    "Integer",
    "Number",
    "String",
    "Array",
    "ArrayOf",
    "Choice",
    "Enumerated",
    "Map",
    "MapOf",
    "Record",
    # Helpers
    "Primitive",
    "Structure",
    "Definition",
    "DefTypes",
    "Field",
    "Options",
    "clsName",
    "custom_def",
    "make_def"
]

# Types
DerivedArg = Union[
    Type[Union[ArrayOf, MapOf]],
    Dict[str, Tuple[str, FieldInfo]]
]


def clsName(name: str) -> str:
    name = re.sub(r"[\-\s]", "_", name)
    return name


def custom_def(name: str, cls: Type[Definition], opts: Union[dict, list, Options], desc: str = "") -> Type[Definition]:
    alias = clsName(name)
    base_opts = [b.__options__ for b in reversed(cls.__mro__) if issubclass(b, DefinitionBase) and b != DefinitionBase]
    opts = Options(*base_opts, opts, name=name)
    cls_kwargs = {
        "__doc__": desc,
        "__options__": opts
    }
    return create_model(alias, __base__=cls, __cls_kwargs__=cls_kwargs)


def make_def(data: list, formats: Dict[str, Callable] = None) -> Type[Definition]:
    def_obj = jadn_def(*data)
    if cls := DefTypes.get(def_obj.type):
        cls_kwargs = {}
        fields = {}
        if def_obj.type == "Enumerated":
            values = {}
            for field in def_obj.fields:
                field_obj = dict(enum_field(*field)._asdict())
                field_obj["default"] = field_obj["name"]
                values[field_obj.pop("name")] = Field(**field_obj)
            cls_kwargs["__enums__"] = Enum("__enums__", values)
        else:
            for field in def_obj.fields:
                field_obj = dict(def_field(*field)._asdict())
                field_obj["options"] = Options(field_obj["options"])
                name = field_obj.pop("name")
                if alias := FieldAlias.get(name):
                    field_obj["alias"] = name
                    name = alias

                field_type = clsName(field_obj.get("type", "String"))
                if def_obj.type == "Choice" or field_obj["options"].isOptional():
                    annotation = Optional[field_type]
                    field_obj["required"] = False
                else:
                    annotation = field_type
                    field_obj["required"] = True
                field_info = Field(**field_obj)
                fields[name] = (annotation, field_info)

        alias = clsName(def_obj.name)
        base_opts = [b.__options__ for b in reversed(cls.__mro__) if issubclass(b, DefinitionBase) and b != DefinitionBase]
        cls_kwargs.update(
            __name__=alias,
            __doc__=def_obj.description,
            __options__=Options(*base_opts, def_obj.options, name=def_obj.name, validation=formats)
        )
        def_model = create_model(alias, __base__=cls, __cls_kwargs__=cls_kwargs, **fields)
        return def_model
    raise TypeError(f"Unknown definition of {def_obj.type}")
