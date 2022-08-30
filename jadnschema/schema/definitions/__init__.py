import re
from collections import namedtuple
from enum import Enum
from typing import Callable, Dict, Type, Optional, Union, get_args
from pydantic import Field, create_model

from ..consts import FieldAlias
from .options import Options
from .definitionBase import DefinitionBase
from .primitives import Binary, Boolean, Integer, Number, String
from .structures import Array, ArrayOf, Choice, Map, Enumerated, MapOf, Record

Definition = Union[Binary, Boolean, Integer, Number, String, Array, ArrayOf, Choice, Enumerated, Map, MapOf, Record]

jadn_def = namedtuple('jadn_def', ('name', 'type', 'options', 'description', 'fields'), defaults=(None, None, [], "", []))
def_field = namedtuple('def_field', ('id', 'name', 'type', 'options', 'description'))
enum_field = namedtuple('enum_field', ('id', 'name', 'description'))

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
    "Definition",
    "DefTypes",
    "Field",
    "clsName",
    "custom_def",
    "make_def"
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
                values[field_obj.pop('name')] = Field(**field_obj)
            cls_kwargs["__enums__"] = Enum("__enums__", values)
        else:
            for field in def_obj.fields:
                field_obj = dict(def_field(*field)._asdict())
                field_obj["options"] = Options(field_obj["options"])
                minc = getattr(field_obj["options"], "minc", 0)
                field_obj["required"] = minc is None or (minc or 0) >= 1
                name = field_obj.pop('name')
                if alias := FieldAlias.get(name):
                    field_obj["alias"] = name
                    name = alias

                field_type = clsName(field_obj.get('type', 'String'))
                if def_obj.type == "Choice":
                    annotation = Optional[field_type]
                elif field_obj.get("required", True):
                    annotation = field_type
                else:
                    annotation = Optional[field_type]
                fields[name] = (annotation, Field(**field_obj))

        alias = clsName(def_obj.name)
        base_opts = [b.__options__ for b in reversed(cls.__mro__) if issubclass(b, DefinitionBase) and b != DefinitionBase]
        cls_kwargs.update(
            __name__=alias,
            __doc__=def_obj.description,
            __options__=Options(*base_opts, def_obj.options, name=def_obj.name, validation=formats)
        )
        return create_model(alias, __base__=cls, __cls_kwargs__=cls_kwargs, **fields)
    raise TypeError(f"Unknown definition of {def_obj.type}")
