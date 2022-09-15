from ..utils import EnumBase


# Valid Schema Formats for conversion
class SchemaFormats(str, EnumBase):
    # CDDL = "cddl"
    # HTML = "html"
    # JDIL = "jidl"
    JADN = "jadn"
    # JAS = "jas"
    # MarkDown = "md"
    # Proto = "proto"
    # Relax = "rng"
    # Thrift = "thrift"


# Conversion Comment Level
class CommentLevels(str, EnumBase):
    ALL = "all"
    NONE = "none"


# Conversion
class JsonRootStyle(str, EnumBase):
    Property = "property"  # generate root properties for each exported type
    OneOf = "oneOf"        # generate a oneOf for each exported type


class JsonEnumStyle(str, EnumBase):
    Const = "const"  # generate oneOf keyword with const for each item
    Enum = "enum"    # generate an enum keyword containing all items
    Regex = "regex"  # generate a regular expression that matches each item


class JsonImportStyle(str, EnumBase):
    Any = "any"  # ignore types defined in other modules, validate anything
    Ref = "ref"  # generate $ref keywords that must be resolved before the JSON Schema can validate referenced types