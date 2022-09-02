import json
import numbers

from pathlib import Path
from typing import Any, Callable, Dict, NoReturn, Optional, Set, Type, Union, get_args
from pydantic.main import ModelMetaclass, PrivateAttr
from .baseModel import BaseModel
from .consts import OPTION_ID
from .info import Information
from .definitions import DefTypes, Definition, make_def, make_derived
from .definitions.field import getFieldType
from .formats import ValidationFormats


class SchemaMeta(ModelMetaclass):
    def __new__(mcs, name, bases, attrs, **kwargs):  # pylint: disable=bad-classmethod-argument
        types = attrs.get("types", {})
        derived_types = {}
        if isinstance(types, list):
            types = {td[0]: make_def(td) for td in types}

        for def_cls in types.values():
            if def_cls.data_type in ("ArrayOf", "MapOf"):
                derived = make_derived(def_cls.name, def_cls)

        new_namespace = {
            **attrs,
            "_info": "info" in attrs,
            "_derived_types": derived_types,
            "types": types,
        }
        return super().__new__(mcs, name, bases, new_namespace, **kwargs)


class Schema(BaseModel, metaclass=SchemaMeta):  # pylint: disable=invalid-metaclass
    info: Optional[Information]
    types: dict  # Dict[str, Definition]
    _derived_types: Dict[str, Type[Definition]] = PrivateAttr({})
    _info: bool = PrivateAttr(False)
    __formats__: Dict[str, Callable] = ValidationFormats

    # Pydantic Overrides
    @classmethod
    def parse_obj(cls: Type["Schema"], obj: Any) -> "Schema":
        cls._info = "info" in obj
        types = obj.get("types")
        if isinstance(types, list):
            obj["types"] = {val[0]: make_def(val, cls.__formats__) for val in reversed(types)}

        cls_defs = {d.__name__: d for d in obj["types"].values()}
        cls_defs.update(cls._derived_types)
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
        raise TypeError("Value is not a valid exported type")

    def validate_as(self, type_: str, value: Any) -> Definition:
        if self.info and self.info.exports:
            if type_ not in self.info.exports.json():
                print("Type is not a valid exported definition")
        if cls := self.types.get(type_):
            return cls.validate(value)
        raise TypeError(f"{type_} is not a valid type within the schema")

    # Helpers
    def _dumps(self, schema: Union[dict, float, int, str, tuple], indent: int = 2, _level: int = 0) -> str:
        """
        Properly format a JADN schema
        :param schema: Schema to format
        :param indent: spaces to indent
        :param _level: current indent level
        :return: Formatted JADN schema
        """
        if isinstance(schema, (numbers.Number, str)):
            return json.dumps(schema)

        _indent = indent - 1 if indent % 2 == 1 else indent
        _indent += (_level * 2)
        ind, ind_e = " " * _indent, " " * (_indent - 2)

        if isinstance(schema, dict):
            lines = ",\n".join(f"{ind}\"{k}\": {self._dumps(v, indent, _level + 1)}" for k, v in schema.items())
            return f"{{\n{lines}\n{ind_e}}}"

        if isinstance(schema, (list, tuple)):
            nested = schema and isinstance(schema[0], (list, tuple))  # Not an empty list
            lvl = _level + 1 if nested and isinstance(schema[-1], (list, tuple)) else _level
            lines = [self._dumps(val, indent, lvl) for val in schema]
            if nested:
                return f"[\n{ind}" + f",\n{ind}".join(lines) + f"\n{ind_e}]"
            return f"[{', '.join(lines)}]"
        return "???"

    def dump(self, fname: Union[str, Path]) -> NoReturn:
        output = fname if fname.endswith(".jadn") else f"{fname}.jadn"
        with open(output, "w", encoding="UTF-8") as f:
            f.write(self.dumps())
        pass

    def dumps(self, ind: int = 2) -> str:
        return self._dumps(self.schema(), indent=ind)

    def analyze(self) -> dict:
        def ns(name: str, nsids: dict) -> str:
            # Return namespace if name has a known namespace, otherwise return full name
            nsp = name.split(':')[0]
            return nsp if nsp in nsids else name

        deps = self.dependencies()
        imports = getattr(self.info.namespaces, "value", lambda: {})()
        exports = getattr(self.info.exports, "value", lambda: [])()

        defs = set(deps) | set(imports)
        refs = {ns(r, imports) for i in deps for r in deps[i]} | set(exports)
        oids = (OPTION_ID['enum'], OPTION_ID['pointer'])
        refs = {r[1:] if r[0] in oids else r for r in refs}  # Reference base type for derived enums/pointers
        return {
            "unreferenced": list(map(str, defs - refs)),
            "undefined": list(map(str, refs - defs)),
            "cycles": [],
        }

    def dependencies(self) -> Dict[str, Set[str]]:
        base_deps = {a.name for a in get_args(Definition)}
        base_deps.add(None)
        deps = {}
        for def_cls in self.types.values():
            if def_cls.data_type in ("ArrayOf", "MapOf"):
                deps[def_cls.name] = {
                    def_cls.__options__.get("ktype", "String"),
                    def_cls.__options__.get("vtype", "String")
                } - base_deps
            else:
                fields = def_cls.__fields__
                if "__root__" in fields:
                    deps[def_cls.name] = set()
                else:
                    deps[def_cls.name] = {getFieldType(f) for f in def_cls.__fields__.values()} - base_deps
        return deps
