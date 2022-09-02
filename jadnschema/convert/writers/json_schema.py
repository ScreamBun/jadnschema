"""
JADN to JSON Schema
"""
import json
import re

from typing import Any, Dict, Tuple, Union
from pydantic.fields import ModelField
from .baseWriter import WriterBase
from ..constants import HexChar, IPv4_Addr, IPv4_Mask, IPv6_Addr, IPv6_Mask
from ..enums import CommentLevels, JsonEnumStyle, JsonImportStyle, JsonRootStyle
from ...schema import Schema
from ...schema.definitions import Options, Primitive, Array, ArrayOf, Choice, Enumerated, Map, MapOf, Record

# Constants
EmptyValues = ["", " ", None, (), [], {}]
FieldMap: Dict[str, str] = {
    "Binary": "string",
    "Boolean": "bool",
    "Integer": "integer",
    "Number": "number",
    "Null": "null",
    "String": "string"
}
JADN_FMT: Dict[str, dict] = {
    "eui": {"pattern": fr"^({HexChar}{{2}}[:-]){{5}}{HexChar}{{2}}(([:-]{HexChar}{{2}}){{2}})?$"},
    "ipv4-addr": {"pattern": fr"^{IPv4_Addr}$"},
    "ipv6-addr": {"pattern": fr"^{IPv6_Addr}$"},
    "ipv4-net": {"pattern": fr"^{IPv4_Addr}(\/{IPv4_Mask})?$"},
    "ipv6-net": {"pattern": fr"^{IPv6_Addr}(\/{IPv6_Mask})?$"},
    "i8": {"minimum": -128, "maximum": 127},
    "i16": {"minimum": -32768, "maximum": 32767},
    "i32": {"minimum": -2147483648, "maximum": 2147483647},
    "x": {"contentEncoding": "base16"}
}
OptionKeys: Dict[Tuple[str], Dict[str, str]] = {
    ("array",): {
        "minv": "minItems",
        "maxv": "maxItems",
        "unique": "uniqueItems"
    },
    ("integer", "number"): {
        "minc": "minimum",
        "maxc": "maximum",
        "minf": "minimum",
        "maxf": "maximum",
        "minv": "minimum",
        "maxv": "maximum",
        "format": "format"
    },
    ("choice", "map", "object"): {
        "minv": "minProperties",
        "maxv": "maxProperties"
    },
    ("binary", "enumerated", "string"): {
        "format": "format",
        "minc": "minLength",
        "maxc": "maxLength",
        "minv": "minLength",
        "maxv": "maxLength",
        "pattern": "pattern"
    }
}
SchemaOrder: Tuple[str, ...] = ("$schema", "$id", "title", "type", "$ref", "const", "description",
                                "additionalProperties", "minProperties", "maxProperties", "minItems", "maxItems",
                                "oneOf", "required", "uniqueItems", "items", "format", "contentEncoding", "properties",
                                "definitions")
# JADN: JSON
ValidationMap: Dict[str, Union[str, None]] = {
    # JADN
    "b": "binary",
    "ipv4-addr": "ipv4",
    "ipv6-addr": "ipv6",
    "x": "binary",
    # JSON
    "date-time": "date-time",
    "date": "date",
    "email": "email",
    "hostname": "hostname",
    "idn-email": "idn-email",
    "idn-hostname": "idn-hostname",
    "ipv4": "ipv4",
    "ipv6": "ipv6",
    "iri": "iri",
    "iri-reference": "iri-reference",
    "json-pointer": "json-pointer",  # Draft 6
    "relative-json-pointer": "relative-json-pointer",
    "regex": "regex",
    "time": "time",
    "uri": "uri",
    "uri-reference": "uri-reference",  # Draft 6
    "uri-template": "uri-template",  # Draft 6
}


# Conversion Class
class JADNtoJSON(WriterBase):
    format = "json"
    comment_multi = ("/*", "*/")
    _ignoreOpts: Tuple[str] = ("dir", "id", "ktype", "vtype")

    def dumps(self, **kwargs) -> str:
        return json.dumps(self.schema(**kwargs), indent=2)

    def schema(self, **kwargs) -> dict:
        kwargs.setdefault("enum", JsonEnumStyle.Enum)
        kwargs.setdefault("imp", JsonImportStyle.Any)
        kwargs.setdefault("root", JsonRootStyle.Property)
        json_schema = dict(
            **self.makeHeader(),
            type="object",
            additionalProperties=False
        )

        root = kwargs.get("root", JsonRootStyle.Property)
        exports = self._schema.info.exports.value()
        for exp in exports:
            if cls := self._schema.types.get(exp):
                if root == JsonRootStyle.Property:
                    json_schema.setdefault("properties", {})[cls.name.lower().replace("-", "_")] = {
                        "$ref": self.formatStr(f"#/definitions/{cls.name}"),
                        "description": self._cleanComment(cls.description)
                    }
                elif root == JsonRootStyle.OneOf:
                    json_schema.setdefault("oneOf", []).append({
                        "$ref": self.formatStr(f"#/definitions/{cls.name}"),
                        "description": self._cleanComment(cls.description)
                    })
            else:
                print(f"Exported name `{exp}` is not a valid type within the schema")

        defs = {k: v for d in self._makeStructures(default={}, **kwargs).values() for k, v in d.items()}
        tmp_defs = {k: defs[k] for k in self._definition_order if k in defs}
        tmp_defs.update({k: defs[k] for k in defs if k not in self._definition_order})
        json_schema["definitions"] = tmp_defs
        return self._setOrder(self._cleanEmpty(json_schema))

    def makeHeader(self) -> dict:
        """
        Create the headers for the schema
        :return: header for schema
        """
        module = self._schema.info.get("package", "")
        return self._cleanEmpty({
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": f"{'' if module.startswith('http') else 'http://'}{module}",
            "title": self._schema.info.title if hasattr(self._schema.info, "title") else (module + (f" v.{self._schema.info.patch}" if hasattr(self._schema.info, "patch") else "")),
            "description": self._cleanComment(self._schema.info.get("description", ""))
        })

    # Structure Formats
    def _formatArray(self, itm: Array, **kwargs) -> dict:
        opts = self._optReformat("array", itm.__options__, False)
        if "pattern" in opts:
            array_json = dict(
                title=self.formatTitle(itm.name),
                type="string",
                description=self._cleanComment(itm.description),
                **opts
            )
        else:
            # TODO: finish things
            print(f"Convert Array, unknown typing: {itm.name}")
            array_json = dict(
                title=itm.name.replace("-", " "),
                type="array",
                description=self._cleanComment(itm.description),
                items=[]
            )

        return {self.formatStr(itm.name): self._cleanEmpty(array_json)}

    def _formatArrayOf(self, itm: ArrayOf, **kwargs) -> dict:
        vtype = itm.__options__.get("vtype", "String")
        arrayof_def = dict(
            title=self.formatTitle(itm.name),
            type="array",
            description=self._cleanComment(itm.description),
            **self._optReformat("array", itm.__options__, False)
        )

        if vtype.startswith("$"):
            val_def = list(filter(lambda d: d.name == vtype[1:], self._schema.types))
            val_def = val_def[0] if len(val_def) == 1 else {}
            id_val = val_def.options.get("id", None)
            enum_val = "id" if id_val else ("value" if val_def.type == "Enumerated" else "name")

            arrayof_def["items"] = dict(
                type="integer" if id_val else "string",
                enum=[f.get(enum_val) for f in val_def.fields]
            )
        else:
            arrayof_def["items"] = self._getFieldType(vtype)

        return {self.formatStr(itm.name): self._cleanEmpty(arrayof_def)}

    def _formatChoice(self, itm: Choice, **kwargs) -> dict:
        return {
            self.formatStr(itm.name): self._cleanEmpty(dict(
                title=self.formatTitle(itm.name),
                type="object",
                description=self._cleanComment(itm.description),
                additionalProperties=False,
                minProperties=1,
                maxProperties=1,
                **self._optReformat("object", itm.__options__, False),
                properties={f.alias: self._makeField(f) for f in itm.__fields__.values()}
            ))
        }

    def _formatEnumerated(self, itm: Enumerated, **kwargs) -> dict:
        enum_format = kwargs.get("enum", JsonEnumStyle.Enum)
        use_id = getattr(itm.__options__, "id", False)
        enum_json = self._cleanEmpty(dict(
            title=self.formatTitle(itm.name),
            type="integer" if use_id and enum_format != JsonEnumStyle.Regex else "string",
            description=self._cleanComment(itm.description),
            **self._optReformat("object", itm.__options__, False)
        ))
        if enum_format == JsonEnumStyle.Const:
            enum_json["oneOf"] = [{
                "const": f.value.extra["id"] if use_id else f.value.default,
                "description": self._cleanComment(f"{(f.value.default + ' - ') if use_id else ''}{f.value.description or ''}")
            } for f in itm.__enums__]
        elif enum_format == JsonEnumStyle.Enum:
            enum_json["enum"] = [f.value.extra["id"] if use_id else f.value.default for f in itm.__enums__]
        elif enum_format == JsonEnumStyle.Regex:
            enum_json["pattern"] = f"^({'|'.join(str(f.value.extra['id']) if use_id else f.value.default for f in itm.__enums__)})$"
        return {self.formatStr(itm.name): enum_json}

    def _formatMap(self, itm: Map, **kwargs) -> dict:
        return {
            self.formatStr(itm.name): self._cleanEmpty(dict(
                title=self.formatTitle(itm.name),
                type="object",
                description=self._cleanComment(itm.description),
                additionalProperties=False,
                **self._optReformat("object", itm.__options__, False),
                required=[f.alias for f in itm.__fields__.values() if f.required],
                properties={f.alias: self._makeField(f) for f in itm.__fields__.values()}
            ))
        }

    def _formatMapOf(self, itm: MapOf, **kwargs) -> dict:
        key_type = self._schema.types.get(itm.__options__.get("ktype"))
        if key_type.data_type in ("Choice", "Enumerated", "Map", "Record"):
            if key_type.data_type == "Enumerated":
                key_values = [f.name for f in key_type.__enums__]
            else:
                key_values = [f.alias for f in key_type.__fields__.values()]
            keys = f"^({'|'.join(key_values)})$"
        else:
            print(f"Invalid MapOf definition for {itm.name}")
            keys = "^.*$"

        return {
            self.formatStr(itm.name): self._cleanEmpty(dict(
                title=self.formatTitle(itm.name),
                type="object",
                description=self._cleanComment(itm.description),
                additionalProperties=False,
                minProperties=1,
                patternProperties={
                    keys: self._getFieldType(itm.__options__.get("vtype", "String"))
                }
            ))
        }

    def _formatRecord(self, itm: Record, **kwargs) -> dict:
        return {
            self.formatStr(itm.name): self._cleanEmpty(dict(
                title=self.formatTitle(itm.name),
                type="object",
                description=self._cleanComment(itm.description),
                additionalProperties=False,
                **self._optReformat("object", itm.__options__, False),
                required=[f.alias for f in itm.__fields__.values() if f.required],
                properties={f.alias: self._makeField(f) for f in itm.__fields__.values()}
            ))
        }

    # Primitive Formats
    def _formatCustom(self, itm: Primitive, **kwargs) -> dict:
        custom_json = dict(
            title=self.formatTitle(itm.name),
            **self._getFieldType(itm.data_type),
            description=self._cleanComment(itm.description)
        )

        opts = self._optReformat(itm.data_type, itm.__options__, base_ref=True)
        keys = {*custom_json.keys()}.intersection({*opts.keys()})
        if keys:
            keys = {k: (custom_json[k], opts[k]) for k in keys}
            print(f"{itm.name} Key duplicate - {keys}")

        if any(k in opts for k in ("pattern", "format")):
            custom_json.pop("$ref", None)
            custom_json.pop("format", None)
            custom_json["type"] = "string"

        custom_json.update(opts)
        return {self.formatStr(itm.name): self._cleanEmpty(custom_json)}

    _formatBinary = _formatCustom
    _formatBoolean = _formatCustom
    _formatInteger = _formatCustom
    _formatNumber = _formatCustom
    _formatString = _formatCustom

    # Helpers
    def _optReformat(self, opt_type: str, opts: Options, base_ref: bool = False) -> dict:
        opt_type = opt_type.lower()
        opt_keys = [v for k, v in OptionKeys.items() if opt_type in k]
        opt_keys = opt_keys[0] if len(opt_keys) == 1 else {}
        r_opts = {}

        def ignore(k, v):
            if k in ("object", "array"):
                return False
            if base_ref:
                return False
            if k in ("minc", "maxc", "minv", "maxv"):
                return v == 0
            return False

        for key, val in opts.value(exclude_unset=True).items():
            if ignore(key, val) or key in self._ignoreOpts:
                continue

            if key == "format":
                if fmt := JADN_FMT.get(val):
                    r_opts.update(fmt)
                else:
                    r_opts[opt_keys[key]] = ValidationMap.get(val, val)
            elif key in opt_keys:
                r_opts[opt_keys[key]] = val
            else:
                print(f"unknown option for type of {opt_type}: {key} - {val}")

        if fmt := r_opts.get("format", None):
            if re.match(r"^u\d+$", fmt):
                del r_opts["format"]
                r_opts.update({
                    "minLength" if opt_type in ("Binary", "String") else "minimum": 0,
                    "maxLength" if opt_type in ("Binary", "String") else "maximum": pow(2, int(fmt[1:])) - 1
                })

        return r_opts

    def _getFieldType(self, field: Union[str, ModelField]) -> dict:
        field_type = getattr(getattr(field, "type_", field), "name", field)
        field_type = field_type if isinstance(field_type, str) else "String"

        if isinstance(field, ModelField):
            rtn = {
                "MapOf": self._formatMapOf,
                "ArrayOf": self._formatArrayOf
            }.get(field.type_, lambda f: {})(field)

            if rtn:
                rtn.pop("title", None)
                return rtn
            if field.type_ in FieldMap:
                rtn = {"type": self.formatStr(FieldMap.get(field.type_, field.type_))}
                return rtn

        if field_type in self._customFields:
            return {"$ref": f"#/definitions/{self.formatStr(field_type)}"}
        if field_type in FieldMap:
            return {"type": self.formatStr(FieldMap.get(field_type, field_type))}

        if ":" in field_type:
            src, attr = field_type.split(":", 1)
            if imports := self._schema.info.imports:
                if src in imports:
                    fmt = "" if imports[src].endswith(".json") else ".json"
                    return {"$ref": f"{imports[src]}{fmt}#/definitions/{attr}"}

        if re.match(r"^Enum\(.*?\)$", field_type):
            f_type = self._schema.types.get(field_type[5:-1])
            if f_type.type in ("Array", "Choice", "Map", "Record"):
                return {
                    "type": "string",
                    "description": f"Derived enumeration from {f_type.name}",
                    "enum": [f.name for f in f_type.get("fields", [])]
                }
            raise TypeError(f"Invalid derived enumeration - {f_type.name} should be a Array, Choice, Map or Record type")

        if re.match(r"^MapOf\(.*?\)$", field_type):
            print(f"Derived MapOf - {field_type}")

        print(f"unknown type: {field_type} - {field}")
        return {"type": "string"}

    def _getType(self, name: str) -> str:
        """
        Get the JSON type of the field based of the type defined in JADN
        :param name: type of field as defined in JADN
        :return: type of the field as defined in JSON
        """
        if cls := self._customFields.get(name):
            return cls
        return "String"

    def _makeField(self, field: ModelField) -> dict:
        if field.field_info.extra["options"].isArray():
            field_def = dict(
                type="array",
                items=self._getFieldType(field)
            )
        else:
            field_def = self._getFieldType(field)
            field_def = field_def[field.alias] if len(field_def.keys()) == 1 and field.alias in field_def else field_def

        ref = "$ref" not in field_def and field.type_ in ("Integer", "Number")
        field_type = field_def.get("type", "")
        field_type = field_def.get("$ref", "") if field_type == "" else field_type
        field_type = self._getType(field_type.split("/")[-1]) if field_type.startswith("#") else field_type
        field_opts = self._optReformat(field_type, field.field_info.extra["options"], base_ref=ref)
        if field_def.get("type", "") == "array" and "minItems" not in field_opts:
            field_opts["minItems"] = 1

        field_def.update(
            description=self._cleanComment(field.field_info.description),
            **field_opts
        )
        field_def.pop("title", None)
        if field_def.get("type") != "string":
            field_def.pop("format", None)

        return field_def

    def _cleanComment(self, msg: str, **kargs) -> str:
        if self._comm == CommentLevels.NONE:
            return ""
        return ("" if msg in ["", None, " "] else msg) + "".join(f" #{k}:{json.dumps(v)}" for k, v in kargs.items())

    def _cleanEmpty(self, itm: Any) -> Any:
        if isinstance(itm, dict):
            return {k: self._cleanEmpty(v) for k, v in itm.items() if v not in EmptyValues}
        elif isinstance(itm, (list, tuple, set)):
            tmp = [self._cleanEmpty(i) for i in itm]
            return type(itm)(tmp)
        else:
            return itm

    def _setOrder(self, itm: Any) -> Any:
        if isinstance(itm, dict):
            tmp = {k: self._setOrder(v) for k, v in itm.items()}
            rtn = {k: tmp[k] for k in SchemaOrder if k in tmp}
            rtn.update({k: tmp[k] for k in tmp if k not in SchemaOrder})
            return rtn
        if isinstance(itm, (list, tuple)):
            return [self._setOrder(i) for i in itm]
        return itm


# Writer Functions
def json_dump(schema: Union[str, dict, Schema], fname: str, source: str = "", comm: CommentLevels = CommentLevels.ALL, **kwargs):
    comm = comm if comm in CommentLevels else CommentLevels.ALL
    return JADNtoJSON(schema, comm).dump(fname, source, **kwargs)


def json_dumps(schema: Union[str, dict, Schema], comm: CommentLevels = CommentLevels.ALL, **kwargs):
    comm = comm if comm in CommentLevels else CommentLevels.ALL
    return JADNtoJSON(schema, comm).dumps(**kwargs)
