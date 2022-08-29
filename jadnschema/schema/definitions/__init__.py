import re
from collections import namedtuple
from typing import Type, Union, get_args
from pydantic import Field

from ..consts import FieldAlias
from .options import Options
from .definitionBase import DefinitionBase
from .primitives import Binary, Boolean, Integer, Number, String
from .structures import Array, ArrayOf, Choice, Map, Enumerated, MapOf, Record

Primitive = Union[Binary, Boolean, Integer, Number, String]
Structure = Union[Array, ArrayOf, Choice, Enumerated, Map, MapOf, Record]
Definition = Union[Primitive, Structure]

jadn_def = namedtuple('jadn_def', ('name', 'type', 'options', 'description', 'fields'), defaults=(None, None, [], "", []))
def_field = namedtuple('def_field', ('id', 'name', 'type', 'options', 'description'))
enum_field = namedtuple('enum_field', ('id', 'name', 'description'))

DefTypes = {d.__name__: d for d in get_args(Definition)}


def clsName(name: str) -> str:
    name = re.sub(r"[\-\s]", "_", name)
    return name


def custom_def(name: str, cls: Type[Definition], opts: Union[dict, list, Options], desc: str = "") -> Type[Definition]:
    alias = clsName(name)
    base_opts = [b.__options__ for b in reversed(cls.__mro__) if issubclass(b, DefinitionBase) and b != DefinitionBase]
    opts = Options(*base_opts, opts, name=name)
    return type(alias, (cls,), {
        "__name__": alias,
        "__doc__": desc,
        "__options__": opts
    })


def make_def(data: list) -> Type[Definition]:
    def_obj = jadn_def(*data)
    if cls := DefTypes.get(def_obj.type):
        def_annotations = {}
        def_fields = {}
        for field in def_obj.fields:
            if def_obj.type == "Enumerated":
                field_obj = dict(enum_field(*field)._asdict())
                field_obj["default"] = field_obj["name"]
            else:
                field_obj = dict(def_field(*field)._asdict())
                field_obj["options"] = Options(field_obj["options"])

            name = field_obj.pop('name')
            if alias := FieldAlias.get(name):
                field_obj["alias"] = name
                name = alias

            def_annotations[name] = field_obj.pop('type', 'String')
            def_fields[name] = Field(**field_obj)
        alias = clsName(def_obj.name)
        base_opts = [b.__options__ for b in reversed(cls.__mro__) if issubclass(b, DefinitionBase) and b != DefinitionBase]
        opts = Options(*base_opts, def_obj.options, name=def_obj.name)
        return type(alias, (cls, ), {
            "__name__": alias,
            "__doc__": def_obj.description,
            "__options__": opts,
            "__annotations__": def_annotations,
            **def_fields
        })
    raise TypeError(f"Unknown definition of {def_obj.type}")
