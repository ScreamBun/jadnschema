import re

from typing import Any, Dict, List, Optional
from pydantic import Field, PrivateAttr, validator
from .baseModel import BaseModel


class Namespaces(BaseModel):
    # keyType = NSID
    # valueType = String
    __root__: Dict[str, str]

    def schema(self) -> Dict[str, str]:
        return self.__root__


class Exports(BaseModel):
    __root__: List[str]

    def schema(self) -> List[str]:
        return self.__root__


class Config(BaseModel):
    MaxBinary: Optional[int] = Field(255, alias="$MaxBinary", gt=1)
    MaxString: Optional[int] = Field(255, alias="$MaxString", gt=1)
    MaxElements: Optional[int] = Field(100, alias="$MaxElements", gt=1)
    Sys: Optional[str] = Field("$", alias="$Sys", min_length=1, max_length=1)
    TypeName: Optional[str] = Field(r"^[A-Z][-$A-Za-z0-9]{0,63}$", alias="$TypeName", min_length=1, max_length=127)
    FieldName: Optional[str] = Field(r"^[a-z][_A-Za-z0-9]{0,63}$", alias="$FieldName", min_length=1, max_length=127)
    NSID: Optional[str] = Field(r"^[A-Za-z][A-Za-z0-9]{0,7}$", alias="$NSID", min_length=1, max_length=127)

    def schema(self) -> Dict[str, Any]:
        schema = {}
        for name, conf in self.__fields__.items():
            if (val := getattr(self, name, None)) and val is not None:
                schema[conf.alias] = val
        return schema

    @validator("TypeName", "FieldName", "NSID")
    def regex_check(cls, val: str):  # pylint: disable=no-self-argument
        try:
            re.compile(val)
        except Exception as err:
            raise ValueError from err
        return val


class Information(BaseModel):
    package: Optional[str]
    version: Optional[str]
    title: Optional[str]
    description: Optional[str]
    comment: Optional[str]
    copyright: Optional[str]
    license: Optional[str]
    namespaces: Optional[Namespaces]  # Namespaces
    exports:  Optional[Exports]       # Exports
    config:  Optional[Config]         # Config
    _config: bool = PrivateAttr(False)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._config = "config" in data
        if not self._config:
            self.config = Config()

    def schema(self) -> Dict[str, Any]:
        schema = {}
        for field in self.__fields__:
            if (val := getattr(self, field, None)) and val is not None:
                schema[field] = val.schema() if hasattr(val, "schema") else val
        if not self._config:
            del schema["config"]
        return schema
