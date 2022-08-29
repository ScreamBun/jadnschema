from typing import Any, Dict, Optional, Type
from pydantic.main import ModelMetaclass
from .baseModel import BaseModel
from .info import Information
from .definitions import Definition, make_def


class SchemaMeta(ModelMetaclass):
    def __new__(mcs, name, bases, attrs, **kwargs):
        types = attrs.get("types", {})
        if isinstance(types, list):
            types = {td[0]: make_def(td) for td in types}

        new_namespace = {
            **attrs,
            "types": types
        }
        return super().__new__(mcs, name, bases, new_namespace, **kwargs)


class Schema(BaseModel, metaclass=SchemaMeta):
    info: Optional[Information]
    types: dict  # Dict[str, Definition]

    @classmethod
    def parse_obj(cls: Type['Schema'], obj: Any) -> 'Schema':
        types = obj.get("types")
        if isinstance(types, list):
            obj["types"] = {val[0]: make_def(val) for val in types}
        return super(cls, cls).parse_obj(obj)

    def schema(self) -> Dict[str, Any]:
        schema = {}
        if hasattr(self, "info"):
            schema["info"] = self.info.schema()
        schema.update(types=[d.schema() for d in self.types.values()])
        return schema
