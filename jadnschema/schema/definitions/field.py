from typing import ForwardRef, Union, get_args, get_origin
from pydantic.fields import ModelField  # pylint: disable=no-name-in-module


def getFieldType(field: ModelField) -> str:
    ref = field.type_
    if isinstance(ref, ForwardRef):
        ref = getattr(ref, "__forward_arg__", ref)
        if not isinstance(ref, str):
            return getattr(ref, "name", ref.__name__)
    if get_origin(ref) is Union:
        args = [r for r in get_args(ref) if not issubclass(r, type(None))]
        if len(args) > 1:
            raise TypeError(f"Field {field.alias} is not correctly typed")
        return getattr(args[0], "name", ref)
    return getattr(ref, "name", ref)


def getFieldSchema(field: ModelField) -> list:
    field_extra = field.field_info.extra
    parent = field_extra.get("parent")
    schema = [field_extra.get("id"), field.alias]

    if parent.has_fields():
        opts = field_extra.get("options")
        schema.append(getFieldType(field))
        schema.append(opts.schema())
    schema.append(field.field_info.description or "")
    return schema
