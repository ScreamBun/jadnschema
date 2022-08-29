from pydantic.fields import ModelField


def getFieldSchema(field: ModelField) -> list:
    field_extra = field.field_info.extra
    parent = field_extra.get("parent")
    name = field.default if parent.is_enum() else field.alias
    schema = [field_extra.get("id"), name]

    if parent.has_fields() and not parent.is_enum():
        opts = field_extra.get("options")
        ref = field.type_
        ref = getattr(ref, "__forward_arg__", ref)
        if not isinstance(ref, str):
            ref = getattr(ref, "name", ref.__name__)
        schema.append(ref)
        schema.append(opts.schema())
    schema.append(field.field_info.description or "")
    return schema
