"""
Utility functions & classes
"""
from .general import (
    addKey, check_values, classproperty, default_decode, default_encode, ellipsis_str, floatString, isBase64, safe_cast, toStr, unixTimeMillis
)
from .enums import EnumBase
from .ext_dicts import ObjectDict, FrozenDict, QueryDict

__all__ = [
    # General
    "addKey",
    "check_values",
    "classproperty",
    "default_decode",
    "default_encode",
    "ellipsis_str",
    "floatString",
    "isBase64",
    "safe_cast",
    "toStr",
    "unixTimeMillis",
    # Enums
    "EnumBase",
    # Extended Dicts
    "ObjectDict",
    "FrozenDict",
    "QueryDict"
]
