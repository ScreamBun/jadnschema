import inspect

from typing import Callable, Dict, List, Optional, Tuple, Union
from pydantic import Extra, root_validator
from ..baseModel import BaseModel
from ..consts import ALLOWED_TYPE_OPTIONS, REQUIRED_TYPE_OPTIONS, OPTIONS, OPTION_ID, TYPE_OPTION_KEYS, FIELD_OPTION_KEYS
from ..formats import ValidationFormats


class Options(BaseModel):
    # Custom Options
    data_type: str = ""
    name: Optional[str] = ""
    validation: Dict[str, Callable] = ValidationFormats
    __custom__ = ["data_type", "name", "validation"]
    # Type Options
    id: Optional[bool]         # 61 - "=" Items and Fields are denoted by FieldID rather than FieldName (Section 3.2.1.1)
    vtype: Optional[str]       # 42 - "*" Value type for ArrayOf and MapOf (Section 3.2.1.2)
    ktype: Optional[str]       # 43 - "+" Key type for MapOf (Section 3.2.1.3)
    enum: Optional[str]        # 35 - "#" Extension: Enumerated type derived from a specified type (Section 3.3.3)
    pointer: Optional[str]     # 62 - ">" Extension: Enumerated type pointers derived from a specified type (Section 3.3.5)
    format: Optional[str]      # 47 - "/" Semantic validation keyword (Section 3.2.1.5)
    pattern: Optional[str]     # 37 - "%" Regular expression used to validate a String type (Section 3.2.1.6)
    minf: Optional[float]      # 121 - "y" Minimum real number value (Section 3.2.1.7)
    maxf: Optional[float]      # 122 - "z" Maximum real number value
    minv: Optional[int]        # 123 - "{" Minimum integer value, octet or character count, or element count (Section 3.2.1.7)
    maxv: Optional[int]        # 125 - "}" Maximum integer value, octet or character count, or element count
    unique: Optional[bool]     # 113 - "q" ArrayOf instance must not contain duplicate values (Section 3.2.1.8)
    set: Optional[bool]        # 115 - "s" ArrayOf instance is unordered and unique (Section 3.2.1.9)
    unordered: Optional[bool]  # 98 - "b" ArrayOf instance is unordered (Section 3.2.1.10)
    extend: Optional[bool]     # 88 - "X" Type is extensible; new Items or Fields may be appended (Section 3.2.1.11)
    default: Optional[str]     # 33 - "!" Default value (Section 3.2.1.12)
    # Field options
    minc: Optional[int]        # 91 - "[" Minimum cardinality, default = 1, 0 = optional (Section 3.2.2.1)
    maxc: Optional[int]        # 93 - "]" Maximum cardinality, default = 1, 0 = default max, >1 = array
    tagid: Optional[str]       # enumerated -> 38 - "&" Field containing an explicit tag for this Choice type (Section 3.2.2.2)
    dir: Optional[bool]        # 60 - "<" Pointer enumeration treats field as a group of items (Extension: Section 3.3.5)
    key: Optional[bool]        # 75 - "K" Field is a primary key for this type (Extension: Section 3.3.6)
    link: Optional[bool]       # 76 - "L" Field is a foreign key reference to a type instance (Extension: Section 3.3.6)

    def __init__(self, *args, **kwargs):
        data = {}
        for arg in args:
            if isinstance(arg, list):
                data.update(self.list2dict(arg))
            elif isinstance(arg, dict):
                data.update(arg)
            elif inspect.isclass(arg) or isinstance(arg, Options):
                data.update({k: getattr(arg, k) for k in self.__fields__ if getattr(arg, k, None) is not None})
        data.update(kwargs)
        super().__init__(**data)

    def schema(self) -> List[str]:
        rslt = []
        for field in self.__fields__:
            val = getattr(self, field)
            if field not in self.__custom__ and val is not None:
                if val is True:
                    rslt.append(f"{OPTION_ID.get(field)}")
                else:
                    rslt.append(f"{OPTION_ID.get(field)}{val}")
        return rslt

    # Validation
    @root_validator(pre=True)
    def validate(cls, opts: dict):  # pylint: disable=no-self-argument
        if fields := set(opts.keys()) - set(cls.__custom__):
            data_type = opts.get("data_type")
            if required := set(REQUIRED_TYPE_OPTIONS.get(data_type, ())):
                if missing := (required - fields):
                    raise ValueError(f"{data_type} missing required option of {missing.pop()}")
            if allowed := set(ALLOWED_TYPE_OPTIONS.get(data_type, ())):
                if extra := (fields - allowed):
                    raise ValueError(f"{data_type} has extra options of {extra}")
        return opts

    # Helpers
    @classmethod
    def list2dict(cls, opts: List[str]) -> Dict[str, Union[bool, int, float, str]]:
        rslt = {}
        for opt in opts:
            key, val = opt[0], opt[1:]
            if args := OPTIONS.get(ord(key)):
                rslt[args[0]] = args[1](val)
            else:
                raise KeyError(f"Unknown option id of {key}")
        return rslt

    def isArray(self) -> bool:
        if self.ktype or self.vtype:
            return False
        return (self.maxc or 1) != 1

    def isOptional(self) -> bool:
        return self.get("minc", 1) == 0

    def isRequired(self) -> bool:
        return not self.isOptional()

    def split(self) -> Tuple["Options", "Options"]:
        field_opts = Options({f: self[f] for f in self.__fields__ if f in FIELD_OPTION_KEYS and self[f] is not None})
        type_opts = Options({f: self[f] for f in self.__fields__ if f in TYPE_OPTION_KEYS if self[f] is not None})
        return field_opts, type_opts

    class Config:
        extra = Extra.forbid
        smart_union = True
        fields = {
            "data_type": {"exclude": True},
            "name": {"exclude": True},
            "validation": {"exclude": True}
        }
