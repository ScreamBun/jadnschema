from typing import Any, Dict, List, Optional
from pydantic import Field
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
    MaxBinary: int = Field(alias="$MaxBinary", gt=1)
    MaxString: int = Field(alias="$MaxString", gt=1)
    MaxElements: int = Field(alias="$MaxElements", gt=1)
    Sys: str = Field(alias="$Sys", min_length=1, max_length=1)
    TypeName: str = Field(alias="$TypeName", min_length=1, max_length=127)
    FieldName: str = Field(alias="$FieldName", min_length=1, max_length=127)
    NSID: str = Field(alias="$NSID", min_length=1, max_length=127)

    def schema(self) -> Dict[str, Any]:
        schema = {}
        for name, conf in self.__fields__.items():
            if (val := getattr(self, name, None)) and val is not None:
                schema[conf.alias] = val
        return schema


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

    def schema(self) -> Dict[str, Any]:
        schema = {}
        for field in self.__fields__:
            if (val := getattr(self, field, None)) and val is not None:
                schema[field] = val.schema() if hasattr(val, "schema") else val
        return schema
