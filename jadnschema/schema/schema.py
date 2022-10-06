import json

from numbers import Number
from pathlib import Path
from typing import Any, Callable, Dict, List, NoReturn, Optional, Set, Type, Union, get_args
from pydantic import Field
from pydantic.main import ModelMetaclass, PrivateAttr  # pylint: disable=no-name-in-module
from .baseModel import BaseModel
from .consts import OPTION_ID
from .info import Information
from .definitions import DefTypes, Definition, make_def
from .definitions.field import getFieldType
# from .extensions import unfold_extensions
from .formats import ValidationFormats
from ..exceptions import FormatError, SchemaException


class SchemaMeta(ModelMetaclass):
    def __new__(mcs, name, bases, attrs, **kwargs):  # pylint: disable=bad-classmethod-argument
        types = attrs.get("types", {})

        if isinstance(types, list):
            # info = Information(**attrs.get("info", {}))
            # types = unfold_extensions(types, info.config.Sys)
            types = {td[0]: make_def(td) for td in types}

        new_namespace = {
            **attrs,
            "_info": "info" in attrs,
            "types": types
        }
        return super().__new__(mcs, name, bases, new_namespace, **kwargs)  # pylint: disable=too-many-function-args


class Schema(BaseModel, metaclass=SchemaMeta):  # pylint: disable=invalid-metaclass
    info: Optional[Information] = Field(default_factory=Information)
    types: dict  # Dict[str, Definition]
    _info: bool = PrivateAttr(False)
    __formats__: Dict[str, Callable] = ValidationFormats

    # Pydantic Overrides
    @classmethod
    def parse_obj(cls: Type["Schema"], obj: dict) -> "Schema":
        cls._info = "info" in obj
        types = obj.get("types")

        if isinstance(types, list):
            # info = Information(**obj.get("info", {}))
            # obj["types"] = unfold_extensions(types, info.config.Sys)
            obj["types"] = {val[0]: make_def(val, cls.__formats__) for val in reversed(obj["types"])}

        cls_defs = {d.__name__: d for d in obj["types"].values()}
        cls_defs.update(DefTypes)
        for def_cls in obj["types"].values():
            def_cls.update_forward_refs(**cls_defs)
        obj["types"] = dict(reversed(obj["types"].items()))
        return super(cls, cls).parse_obj(obj)

    def schema(self) -> Dict[str, Any]:
        schema = {}
        if self._info:
            schema["info"] = self.info.schema()
        schema.update(types=[d.schema() for d in self.types.values()])
        return schema

    # Validation
    def validate(self, value: Any) -> Definition:
        if self.info:
            if self.info.exports:
                for export in self.info.exports:
                    return self.validate_as(export[0], value)
        raise SchemaException("Value is not a valid exported type")

    def validate_as(self, type_: str, value: Any) -> Definition:
        if self.info and self.info.exports:
            if type_ not in self.info.exports.json():
                print("Type is not a valid exported definition")
        if cls := self.types.get(type_):
            return cls.validate(value)
        raise SchemaException(f"{type_} is not a valid type within the schema")

    # Helpers
    def _dumps(self, val: Union[dict, float, int, str, tuple, Number], indent: int = 2, _level: int = 0) -> str:
        """
        Properly format a JADN schema
        :param val: value to format
        :param indent: spaces to indent
        :param _level: current indent level
        :return: Formatted JADN schema
        """
        if isinstance(val, (Number, str)):
            return json.dumps(val)

        _indent = indent - 1 if indent % 2 == 1 else indent
        _indent += (_level * 2)
        ind, ind_e = " " * _indent, " " * (_indent - 2)

        if isinstance(val, dict):
            lines = ",\n".join(f"{ind}\"{k}\": {self._dumps(v, indent, _level+1)}" for k, v in val.items())
            return f"{{\n{lines}\n{ind_e}}}"

        if isinstance(val, (list, tuple)):
            nested = val and isinstance(val[0], (list, tuple))  # Not an empty list
            lvl = _level+1 if nested and isinstance(val[-1], (list, tuple)) else _level
            lines = [self._dumps(v, indent, lvl) for v in val]
            if nested:
                return f"[\n{ind}" + f",\n{ind}".join(lines) + f"\n{ind_e}]"
            return f"[{', '.join(lines)}]"
        return "???"

    def _dependencies(self) -> Dict[str, Set[str]]:
        base_deps = {a.name for a in get_args(Definition)}
        base_deps.update({None, ""})
        deps = {}
        for def_cls in self.types.values():
            if def_cls.data_type in ("ArrayOf", "MapOf"):
                deps[def_cls.name] = {
                    def_cls.__options__.get("ktype", "String"),
                    def_cls.__options__.get("vtype", "String")
                } - base_deps
            elif def_cls.has_fields():
                fields = def_cls.__fields__
                if "__root__" in fields:
                    deps[def_cls.name] = {
                        def_cls.__options__.get("ktype", "String"),
                        def_cls.__options__.get("vtype", "String")
                    } - base_deps
                else:
                    field_deps = set()
                    for f in fields.values():
                        field_deps.add(getFieldType(f))
                        if f.field_info.extra["type"] in ("ArrayOf", "MapOf"):
                            field_deps.update({
                                f.field_info.extra["options"].get("ktype"),
                                f.field_info.extra["options"].get("vtype")
                            })
                    deps[def_cls.name] = field_deps - base_deps
            else:
                deps[def_cls.name] = {def_cls.data_type, } - base_deps

        return deps

    def addFormat(self, fmt: str, fun: Callable[[Any], Optional[List[Exception]]], override: bool = False) -> NoReturn:
        """
        Add a format validation function
        :param fmt: format to validate
        :param fun: function that performs the validation
        :param override: override the format if it exists
        :return: None
        """
        if fmt in self.__formats__ and not override:
            raise FormatError(f"format {fmt} is already defined, use `override=True` to override format validation")
        self.__formats__[fmt] = fun

    def analyze(self) -> dict:
        """
        Analyze the given schema for unreferenced and undefined types
        :return: analysis results
        """
        def ns(name: str, nsids: dict) -> str:
            # Return namespace if name has a known namespace, otherwise return full name
            nsp = name.split(':')[0]
            return nsp if nsp in nsids else name

        type_deps = self._dependencies()
        imports = getattr(self.info.namespaces, "value", lambda: {})()
        exports = getattr(self.info.exports, "value", lambda: [])()

        defs = set(type_deps) | set(imports)
        refs = {ns(r, imports) for d in type_deps.values() for r in d} | set(exports)
        oids = (OPTION_ID['enum'], OPTION_ID['pointer'])
        refs = {r[1:] if r[0] in oids else r for r in refs}  # Reference base type for derived enums/pointers
        return {
            "unreferenced": list(map(str, defs - refs)),
            "undefined": list(map(str, refs - defs)),
            "cycles": [],
        }

    def dump(self, fname: Union[str, Path], ind: int = 2) -> NoReturn:
        output = fname if fname.endswith(".jadn") else f"{fname}.jadn"
        with open(output, "w", encoding="UTF-8") as f:
            f.write(self.dumps(ind))

    def dumps(self, ind: int = 2) -> str:
        return self._dumps(self.schema(), indent=ind)
