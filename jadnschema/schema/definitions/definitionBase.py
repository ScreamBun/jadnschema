"""
JADN Definition BaseModel
Customized from `jadnschema.schema.baseModel.BaseModel`
"""
from enum import Enum
from typing import ClassVar
from pydantic import create_model  # pylint: disable=no-name-in-module
from pydantic.main import ModelMetaclass  # pylint: disable=no-name-in-module
from .options import Options
from .field import getFieldSchema
from ..consts import SELECTOR_TYPES, STRUCTURED_TYPES, FIELD_TYPES
from ..baseModel import BaseModel
from ...utils import classproperty, ellipsis_str
__pdoc__ = {
    "DefinitionBase.name": "The definition's valid schema name",
    "DefinitionBase.description": "The definition's description",
    "DefinitionBase.data_type": "The definition's base datatype"
}


class DefinitionMeta(ModelMetaclass):
    def __new__(mcs, name, bases, attrs, **kwargs):  # pylint: disable=bad-classmethod-argument
        base_opts = [b.__options__ for b in reversed(bases) if issubclass(b, BaseModel) and b != BaseModel]
        opts = Options(
            *base_opts,
            attrs.pop("__options__", None), attrs.pop("Options", None),
            kwargs.pop("__options__", None), kwargs.pop("Options", None),
            getattr(mcs, "__options__", None), getattr(mcs, "Options", None),
        )
        new_namespace = {
            **attrs,
            **kwargs,
            "__options__": opts,
        }
        cls = super().__new__(mcs, name, bases, new_namespace)  # pylint: disable=too-many-function-args
        base_names = [b.__name__ for b in bases]
        for idx, (field, opts) in enumerate(cls.__fields__.items()):
            if field != "__root__":
                opts.field_info.extra["parent"] = cls
                field_opts = opts.field_info.extra.setdefault("options", Options())
                opts.field_info.extra.setdefault("id", idx)
                if not opts.required and field_opts.minc != 0 and "Choice" not in base_names:
                    field_opts.minc = 0
        return cls


class DefinitionBase(BaseModel, metaclass=DefinitionMeta):  # pylint: disable=invalid-metaclass
    __options__: ClassVar[Options]

    def __str__(self):
        cls = self.__class__
        mro = [c for c in cls.__mro__ if not c.__name__ == cls.__name__][0]
        data = self.json(exclude_none=True)
        return f"{self.name}({mro.__name__}: {ellipsis_str(data)})"

    # Pydantic overrides
    @classmethod
    def schema(cls) -> list:
        """
        Format the definition to valid JADN schema format
        :return: formatted JADN
        """
        mro = [c for c in cls.__mro__ if not c.__name__ == cls.__name__][0]
        schema = [cls.name, mro.__name__, cls.__options__.schema(), (cls.__doc__ or "").strip()]
        if cls.__fields__ and "__root__" not in cls.__fields__:
            fields = []
            for opt in cls.__fields__.values():
                fields.append(getFieldSchema(opt))
            schema.append(fields)
        return schema

    # Custom Methods
    @classmethod
    def is_enum(cls) -> bool:
        """
        Determine if the definition is an enumerated type
        :return: True/False if the definition is an enumerated type
        """
        for base in cls.__mro__:
            if base.__name__ == "Enumerated":
                return True
        return False

    @classmethod
    def is_structure(cls) -> bool:
        """
        Determine if the definition is a structure type
        `Array`, `ArrayOf`, `Map`, `MapOf`, & `Record` are structure types
        :return: True/False if the definition is a structure type
        """
        for base in cls.__mro__:
            if base.__name__ in STRUCTURED_TYPES:
                return True
        return False

    @classmethod
    def is_selector(cls) -> bool:
        """
        Determine if the definition is a selector type
        `Enumerated` & `Choice` are selector types
        :return: True/False if the definition is a selector type
        """
        for base in cls.__mro__:
            if base.__name__ in SELECTOR_TYPES:
                return True
        return False

    @classmethod
    def has_fields(cls) -> bool:
        """
        Determine if the definition has fields
        `Enumerated`, `Choice`, `Array`, `Map`, & `Record` should have defined fields
        :return: True/False if the definition has fields
        """
        for base in cls.__mro__:
            if base.__name__ in FIELD_TYPES:
                return True
        return False

    # Helpers
    @classproperty
    def name(cls) -> str:  # pylint: disable=no-self-argument
        """The definition's valid schema name"""
        return cls.__options__.name or cls.__name__

    @classproperty
    def description(cls) -> str:  # pylint: disable=no-self-argument
        """The definition's description"""
        return cls.__doc__

    @classproperty
    def data_type(cls) -> str:  # pylint: disable=no-self-argument
        """The definition's base datatype"""
        return cls.__options__.data_type

    @classmethod
    def enumerated(cls) -> "Enumerated":  # pylint: disable=no-self-argument
        """
        Convert the given class to an 'Enumerated' class if applicable
        :return: converted Enumerated class object
        """
        if cls.data_type in ("Binary", "Boolean", "Integer", "Number", "Null", "String"):
            raise TypeError(f"{cls.name} cannot be extended as an enumerated type")

        if cls.data_type == "Enumerated":
            return cls

        from .structures import Enumerated  # pylint: disable=import-outside-toplevel
        name = f"Enum-{cls.name}"
        cls_kwargs = dict(
            __name__=name,
            __doc__=f"Derived Enumerated from {cls.name}",
            __enums__=Enum("__enums__", cls.__fields__),
            __options__=Options(cls.__options__, name=name)
        )
        return create_model(name, __base__=Enumerated, __cls_kwargs__=cls_kwargs)

    class Config:
        arbitrary_types_allowed = True
