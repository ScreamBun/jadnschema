"""
JADN Schema conversion consts
"""
from typing import Dict, Tuple, Union
from ...constants import HexChar, IPv4_Addr, IPv4_Net, IPv6_Addr, IPv6_Net

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
    "ipv4-net": {"pattern": fr"^{IPv4_Net}$"},
    "ipv6-net": {"pattern": fr"^{IPv6_Net}$"},
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
