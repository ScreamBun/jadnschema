from typing import Any, Mapping, Set, Tuple, Union
from pydantic import BaseModel as pydanticBase, Extra

IntStr = Union[int, str]
UntStrMapUnion = Union[Set[IntStr], Mapping[IntStr, Any]]


class BaseModel(pydanticBase):
    # Helpers
    def value(self, *, include: UntStrMapUnion = None, exclude: UntStrMapUnion = None, by_alias: bool = True, skip_defaults: bool = None, exclude_unset: bool = True, exclude_defaults: bool = False, exclude_none: bool = False) -> Any:  # pylint: disable=W0221
        """
        Generate a representation of the model, optionally specifying which fields to include or exclude.
        :param include: fields to include in the returned dictionary; see below
        :param exclude: fields to exclude from the returned dictionary; see below
        :param by_alias: whether field aliases should be used as keys in the returned dictionary; default False
        :param skip_defaults: whether field defaults should be included returned dictionary; default False
        :param exclude_unset: whether fields which were not explicitly set when creating the model should be excluded from the returned dictionary; default False. Prior to v1.0, exclude_unset was known as skip_defaults; use of skip_defaults is now deprecated
        :param exclude_defaults: whether fields which are equal to their default values (whether set or otherwise) should be excluded from the returned dictionary; default False
        :param exclude_none: whether fields which are equal to None should be excluded from the returned dictionary; default False
        :return: representation of the model
        """
        data = self.dict(include=include, exclude=exclude, by_alias=by_alias, skip_defaults=skip_defaults, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none)
        if "__root__" in data:
            return data["__root__"]
        return data

    # Dict like functions
    def __getitem__(self, item: str) -> Any:
        if item in self.__fields__:
            return getattr(self, item, None)
        raise AttributeError(f"{self.__class__.__name__} does not contain {item} as an attribute")

    def __setitem__(self, key: str, value: Any) -> None:
        if key in self.__fields__:
            return setattr(self, key, value)
        raise AttributeError(f"{self.__class__.__name__} does not contain {key} as an attribute")

    def get(self, attr: str, default: Any = None):
        if attr in self.__fields__:
            return getattr(self, attr, default)
        raise KeyError(f"{attr} is not a valid key of {self.__class__.__name__}")

    def keys(self) -> Tuple[str, ...]:
        return tuple(attr for attr in self.__fields__ if self[attr])

    def items(self) -> Tuple[Tuple[str, Any], ...]:
        return tuple(self.dict(by_alias=True, exclude_unset=True).items())

    def update(self, kv: Mapping = None, **kwargs) -> None:
        for k, v in self.__class__(**{**(kv or {}), **kwargs}).items():
            setattr(self, k, v)

    def values(self) -> Tuple[Any, ...]:
        d = self.dict(by_alias=True, exclude_unset=True)
        return tuple(d)

    class Config:
        extra = Extra.forbid
