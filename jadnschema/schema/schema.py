from typing import Any, Callable, Dict, List, Optional, Type
from pydantic.main import ModelMetaclass
from .baseModel import BaseModel
from .info import Information
from .definitions import *
from .formats import ValidationFormats


class SchemaMeta(ModelMetaclass):
    def __new__(mcs, name, bases, attrs, **kwargs):
        types = attrs.get("types", {})
        if isinstance(types, list):
            types = {td[0]: make_def(td) for td in types}

        for t in types.values():
            t.update_forward_refs()

        new_namespace = {
            **attrs,
            "types": types
        }
        return super().__new__(mcs, name, bases, new_namespace, **kwargs)


class Schema(BaseModel, metaclass=SchemaMeta):
    info: Optional[Information]
    types: dict  # Dict[str, Type[Definition]]
    __formats__: Dict[str, Callable] = ValidationFormats

    @classmethod
    def parse_obj(cls: Type['Schema'], obj: Any) -> 'Schema':
        types = obj.get("types")
        if isinstance(types, list):
            obj["types"] = {val[0]: make_def(val, cls.__formats__) for val in reversed(types)}

        cls_defs = {d.__name__: d for d in obj["types"].values()}
        cls_defs.update(DefTypes)
        for def_cls in obj["types"].values():
            def_cls.update_forward_refs(**cls_defs)
        obj["types"] = dict(reversed(obj["types"].items()))
        return super(cls, cls).parse_obj(obj)

    def schema(self) -> Dict[str, Any]:
        schema = {}
        if hasattr(self, "info"):
            schema["info"] = self.info.schema()
        schema.update(types=[d.schema() for d in self.types.values()])
        return schema

    # Validation
    def validate(self, value: Any):
        if self.info:
            if self.info.exports:
                for export in self.info.exports:
                    if err := self.validate_as(export[0], value):
                        raise err[0]
                    return
        raise TypeError(f"Value is not a valid exported type")

    def validate_as(self, type_: str, value: Any) -> Definition:
        if self.info and self.info.exports:
            if type_ not in self.info.exports.json():
                print("Type is not a valid exported definition")
        if cls := self.types.get(type_):
            return cls.validate(value)
        raise TypeError(f"{type_} is not a valid type within the schema")
