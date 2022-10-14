"""
JADN conversions
"""
from .enums import SchemaFormats, CommentLevels, JsonEnumStyle, JsonImportStyle, JsonRootStyle
# from .readers import ()
from .writers import (
    # Writers
    # JADNtoCDDL,
    JADNtoGraphViz,
    JADNtoHTML,
    # JADNtoIDL,
    JADNtoJADN,
    # JADNtoJAS,
    JADNtoJSON,
    JADNtoMD,
    # JADNtoProto3,
    JADNtoRelaxNG,
    # JADNtoThrift,
    # Convert Functions
    # cddl_dump, cddl_dumps,
    dot_dump, dot_dumps,
    html_dump, html_dumps,
    jadn_dump, jadn_dumps,
    # jidl_dump, jidl_dumps,
    # jas_dump, jas_dumps,
    json_dump, json_dumps,
    md_dump, md_dumps,
    # proto_dump, proto_dumps,
    relax_dump, relax_dumps,
    # thrift_dump, thrift_dumps
)


__all__ = [
    # Enums
    "SchemaFormats",
    "CommentLevels",
    "JsonEnumStyle",
    "JsonImportStyle",
    "JsonRootStyle",
    # Convert to ...
    # "cddl_dump",
    # "cddl_dumps",
    "dot_dump",
    "dot_dumps",
    "html_dump",
    "html_dumps",
    "jadn_dump",
    "jadn_dumps",
    # "jas_dump",
    # "jas_dumps",
    # "jidl_dump",
    # "jidl_dumps",
    "json_dump",
    "json_dumps",
    "md_dump",
    "md_dumps",
    # "proto_dump",
    # "proto_dumps",
    "relax_dump",
    "relax_dumps",
    # "thrift_dump",
    # "thrift_dumps",
    # Load From ...
    # "cddl_load",
    # "cddl_loads",
    # "jadn_load",
    # "jadn_loads",
    # "jas_load",
    # "jas_loads",
    # "jidl_load",
    # "jidl_loads",
    # "json_load",
    # "json_loads",
    # "proto_load",
    # "proto_loads",
    # "relax_load",
    # "relax_load",
    # "thrift_load",
    # "thrift_loads",
    # Dynamic
    # "dump",
    # "dumps",
    # "load",
    # "loads"
]
