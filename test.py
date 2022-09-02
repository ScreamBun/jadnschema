import json
import numbers

from typing import Union
from jadnschema.schema import Schema
from oc2ls_v11 import OpenC2LangV11

schema_file = "oc2ls-v1.1-lang_resolved.jadn"


def pretty_jadn(schema: Union[dict, float, int, str, tuple], indent: int = 2, _level: int = 0) -> str:
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
        lines = ",\n".join(f"{ind}\"{k}\": {pretty_jadn(v, indent, _level + 1)}" for k, v in schema.items())
        return f"{{\n{lines}\n{ind_e}}}"

    if isinstance(schema, (list, tuple)):
        nested = schema and isinstance(schema[0], (list, tuple))  # Not an empty list
        lvl = _level + 1 if nested and isinstance(schema[-1], (list, tuple)) else _level
        lines = [pretty_jadn(val, indent, lvl) for val in schema]
        if nested:
            return f"[\n{ind}" + f",\n{ind}".join(lines) + f"\n{ind_e}]"
        return f"[{', '.join(lines)}]"
    return "???"


if __name__ == "__main__":
    schema_code = OpenC2LangV11()
    print(f"Loading code: {OpenC2LangV11.__name__}")
    jadn_obj = schema_code.schema()
    with open("oc2ls-v1.1-lang_resolved.code.jadn", "w") as f:
        f.write(pretty_jadn(jadn_obj))

    print("-"*100)
    # schema_obj = jadn.load(schema_file)
    print(f"Loading file: {schema_file}")
    schema_obj = Schema.parse_file(schema_file)
    jadn_obj = schema_obj.schema()
    with open("oc2ls-v1.1-lang_resolved.load.jadn", "w") as f:
        f.write(pretty_jadn(jadn_obj))
